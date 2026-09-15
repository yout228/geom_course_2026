Wells.csv:
    wells.csv — координаты и измерения в наблюдательных скважинах;
    well_id,radius_m,azimuth_deg,x_m,y_m,pressure_mpa,temperature_c,quality_flag

Layers.xslx:
    layers.xlsx — свойства четырёх слоёв
    layer	top_depth_m	bottom_depth_m	thickness_m	kx_m2	ky_m2	porosity_fraction	compressibility_1_pa
   

pumping_test.txt:
    pumping_test.txt — изменение давления во времени
    time_h  boundary_pressure_mpa  well_pressure_mpa       stage

1 Чем DataFrame отличается от массива NumPy?
    NumPy — это однородныq массив.
    DataFrame — это табличные данные: разные типы столбцов, метки, фильтрация, группировка, соединения, работа с пропусками.

2 Что означают две величины в shape массива (13, 2)?
    Размер по каждому измерению. Это таблица из 13 строк и 2 столбцов.
3 Почему pressure * 1_000_000 не требует цикла for?
    Это векторизированная операция.Векторизованная операция выполняет одно действие сразу для всех элементов столбца или массива
4 Что выбирает срез array[::2]?
    Каждое второе значение
5 Что содержится в логической маске?
    Логическая маска — массив значений True и False. Он показывает, какие строки нужно оставить.
6 Зачем после сохранения загружать массив обратно?
    Для сравнения с исходными.
7 Какие файлы являются исходными, а какие создаются программой?
    Исходными являются: wells.csv, pumpin_test.txt,layers.xslx
    Создаются программой: wells_clean.csv,table_summary.xslx,pressure_cube.npz,pressure_matrix.npy,results.txt 