def txt_to_csv(txt_file_path, csv_file_path):
    with open(txt_file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    dimensions = lines[0].split(',')
    if len(dimensions) != 2:
        raise ValueError("La primera línea debe contener las dimensiones en el formato 'ancho,alto'")
    try:
        width = int(dimensions[0])
        height = int(dimensions[1])
    except ValueError:
        raise ValueError("Las dimensiones deben ser números enteros")
    
    grid_lines = lines[1:]
    if len(grid_lines) != height:
        raise ValueError(f"Se esperaban {height} líneas de cuadrícula, pero se encontraron {len(grid_lines)}")
    
    for line in grid_lines:
        if len(line) != width:
            raise ValueError(f"Cada línea de la cuadrícula debe tener exactamente {width} caracteres")
    
    grid_data = ''.join(grid_lines)
    
    processed_grid_data = ''
    for char in grid_data:
        if char == '0':
            processed_grid_data += '-'
        else:
            processed_grid_data += char
    
    csv_string = f"{width};;{height};;{grid_data};;{processed_grid_data}"
    
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_string)
    
    print(f"Archivo .csv generado exitosamente en '{csv_file_path}'")
