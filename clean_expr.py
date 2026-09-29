with open('painel_repasses_expr.txt', 'r', encoding='utf-8') as f:
    expr = f.read()

# strip any surrounding backticks and whitespace
expr = expr.strip()
while expr.startswith('`'):
    expr = expr[1:].strip()
while expr.endswith('`'):
    expr = expr[:-1].strip()

print('Cleaned expr length:', len(expr))
print('Starts with:', repr(expr[:60]))
print('Ends with:', repr(expr[-60:]))

with open('clean_painel_repasses_expr.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(expr)
