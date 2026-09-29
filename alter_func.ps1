$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
ALTER FUNCTION [dbo].[Func_JOB_CALCULAR_HONORARIO]
(
    @Job VARCHAR(10),
    @Tipocontrato VARCHAR(1) = 'C' --C-> Comercial , O-> Operacional 
)
RETURNS DECIMAL(18,4)
AS
BEGIN
    DECLARE
        @CodigoCliente      INT,
        @CodigoProduto      INT,
        @CodigoUnidade      INT,
        @CodigoModelo       INT,
        @ModCodigo          INT,
        @DataJob            DATETIME,
        @Faturamento        DECIMAL(18,2) = 0,
        @PercProduto        DECIMAL(18,4) = 0,
        @PercFixo           DECIMAL(18,4) = 0,
        @PercEsc            DECIMAL(18,4) = 0,
        @AcrescEsc          BIT = 0,
        @Honorario          DECIMAL(18,4) = 0,
		@Quant_Modelos      INT = 0;

	IF @Tipocontrato = 'O'
	BEGIN
		SELECT 
			@CodigoCliente = A.CODIGO_CLIENTE,
			@CodigoProduto = A.CODIGO_PRODUTO,
			@CodigoUnidade = A.CODIGO_UNIDADE,
			@DataJob       = A.DATA_RECEBIMENTO,
			@CodigoModelo  = A.MODELO_NEGOCIO
		FROM PROJECT_QBERT_JOBS A WITH (NOLOCK)
		WHERE A.JOB = @Job;
	END
	ELSE
	BEGIN
		SELECT 
			@CodigoCliente = C.CctCliente,
			@CodigoProduto = PTC.PtcProduto,
			@CodigoUnidade = CASE 
                                WHEN C.CctUnidadeFranqCom IS NOT NULL AND C.CctUnidadeFranqCom <> 2153 THEN C.CctUnidadeFranqCom
                                WHEN PU.UNIDADE_ID IS NOT NULL THEN PU.UNIDADE_ID
                                ELSE ISNULL(C.CctUnidadeFranqCom, ISNULL(C.CctUnidadeFranqOp, 2153))
                             END,
			@DataJob       = C.CctDataCadastro,
			@CodigoModelo  = CASE 
                                WHEN C.CctModeloNegocio IS NOT NULL AND C.CctModeloNegocio <> 42 THEN C.CctModeloNegocio
                                WHEN PU.MODELO_NEGOCIO_CODIGO IS NOT NULL THEN PU.MODELO_NEGOCIO_CODIGO
                                ELSE ISNULL(C.CctModeloNegocio, 42)
                             END
		FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
		LEFT JOIN PROJECT_TIPOS_CONTRATOS AS PTC ON PTC.PtcCodigo = C.CctTpContrato
		LEFT JOIN PROJECT_SERVICOS AS PS ON PS.GppCodigo = PTC.PtcProduto
        OUTER APPLY (
            SELECT TOP 1 UNIDADE_ID, MODELO_NEGOCIO_CODIGO
            FROM vw_participantes_unidades PU WITH (NOLOCK) 
            WHERE PU.PARTICIPANTE_ID = C.CctCliente
            ORDER BY PU.ModAtivo DESC, PU.VIGENCIA_INICIO DESC
        ) PU
		WHERE C.CctCodigo = @Job;
	END

    IF @CodigoCliente IS NULL
        RETURN 0;

    -- Busca o Modelo da Vigência
	SELECT TOP 1
		@ModCodigo = M.ModCodigo
	FROM SMART_UNIDADES_MODELOS M WITH (NOLOCK)
	WHERE M.ModUnidade = @CodigoUnidade
	    AND M.ModTipoContrato = 1 
		AND (M.ModModelo = @CodigoModelo OR @CodigoModelo IS NULL)
	  	AND CONVERT(DATE,ISNULL(@DataJob, GETDATE()),101) BETWEEN
		CONVERT(DATE, ISNULL(ModData,0), 101) AND CONVERT(DATE,ISNULL(ModDataInativo,ModDataTermino), 101)	
	ORDER BY M.ModData DESC;
 
     -- Se não achou na vigência tenta buscar o modelo ativo ou mais recente   
	  IF @ModCodigo IS NULL
	  BEGIN
		SELECT TOP 1 @ModCodigo = M.ModCodigo
		FROM SMART_UNIDADES_MODELOS M WITH (NOLOCK)
		WHERE M.ModUnidade = @CodigoUnidade
          AND M.ModTipoContrato = 1
        ORDER BY M.ModAtivo DESC, M.ModData DESC;
	  END;

     -- se não achar modelo tenta buscar na vw_participantes_unidades
      IF @ModCodigo IS NULL
      BEGIN
        SELECT TOP 1 @Honorario = ISNULL(PU.PERC_FRANQUEADO, 0)
        FROM vw_participantes_unidades PU WITH (NOLOCK)
        WHERE PU.UNIDADE_ID = @CodigoUnidade;

        RETURN ISNULL(@Honorario, 0);
      END;
    
   -- Produto do JOb 
    SELECT 
	    @PercProduto = ISNULL(P.SppPerc, 0),
        @AcrescEsc =ISNULL(P.SppAcrescEsc, 0) 
    FROM SMART_UNIDADES_MODELOS_PERC_PROD P WITH (NOLOCK)
    WHERE P.SppModCodigo = @ModCodigo   AND P.SppProduto = @CodigoProduto
    ORDER BY P.SppCadData DESC;

    -- busca produto na configuração 
    IF EXISTS
    (
        SELECT 1
        FROM SMART_UNIDADES_MODELOS_PERC_PROD P WITH (NOLOCK)
        WHERE P.SppModCodigo = @ModCodigo  AND P.SppProduto = @CodigoProduto
    )
    BEGIN
        SET @Honorario = @PercProduto;
       -- escalonado 
	   IF @AcrescEsc = 0 
	   BEGIN
		SELECT TOP 1
			@PercEsc = ISNULL(E.SpePerc, 0)
		FROM SMART_UNIDADES_MODELOS_PERC_ESC E WITH (NOLOCK)
		WHERE E.SpeModCodigo = @ModCodigo
		  AND @Faturamento >= E.SpeValorIni
		  AND @Faturamento <= E.SpeValorFim
		ORDER BY E.SpeValorIni DESC;

        SET @Honorario = @PercProduto + @PercEsc;
      END;
        RETURN ISNULL(@Honorario, 0);
    END;

   -- Se chegou aqui não tem produto e seta o FIXO
    SELECT TOP 1
        @PercFixo = ISNULL(F.SpfPerc, 0)
    FROM SMART_UNIDADES_MODELOS_PERC_FIXO F WITH (NOLOCK)
    WHERE F.SpfModCodigo = @ModCodigo
    ORDER BY F.SpfCadData DESC;

    -- Se ainda for 0, tenta buscar o percentual do modelo da unidade
    IF @PercFixo = 0 OR @PercFixo IS NULL
    BEGIN
        SELECT TOP 1 @PercFixo = ISNULL(PU.PERC_FRANQUEADO, 0)
        FROM vw_participantes_unidades PU WITH (NOLOCK)
        WHERE PU.UNIDADE_ID = @CodigoUnidade AND PU.TIPO_CONTRATO_CODIGO = 1;
    END;

    SET @Honorario = ISNULL(@PercFixo, 0);
    RETURN ISNULL(@Honorario, 0);
END;
"@
    $cmd.ExecuteNonQuery() | Out-Null
    Write-Host "Function updated successfully on SQL Server!"
} catch {
    Write-Error $_.Exception.Message
} finally {
    $conn.Close()
}
