tabelas =  ["cidades","concessionarias","estados"]

for table in tabelas:
    tbs = {
        f"tb_input_{table}": f"s3_input_table_{table}_v2",
        f"tb_output_{table}": f"s3_output_table_{table}_v2",
    }
    for tb in tbs.values():
        print(tb)
