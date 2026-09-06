#  UNIVERSIDAD  ESTATAL  AMAZÓNICA

Carrera  de  Tecnologías  de  la  Información
Programación  Orientada  a  Objetos  
Semana  12  
Tema:    Programación  Orientada  a  Objetos
Profesor:    Mgs.  Luis  Antonio  Llerena  Ocaña
Alumno:    Danny  Henry  Betancourt  Luzón
2026-2026  


#  Sistema  de  Restaurante  —  restaurante_app

##  Descripción

Sistema  de  consola  en  Python  para  administrar  productos,  usuarios  y  ventas  de un  restaurante.  Esta  versión  corresponde  a  la  Semana  12:  se  toma  como  base  el proyecto  de  la  Semana  11  (venta  de  productos,  relación  usuario-producto  y persistencia  en  JSON)  y  se  mejora  el  rendimiento  de  las  búsquedas  y  consultas que  antes  recorrían  las  listas  completas.


##  Datos  de  ejemplo

Si  al  ejecutar  el  programa  todavía  no  existen  `productos.json`,
`usuarios.json`  ni  `ventas.json`  (primera  ejecución),  se  cargan  automáticamente
estos  datos,  tal  como  se  usaron  en  semanas  anteriores:

-    Restaurante:    Restaurante  Sabor  Lojano
-    Productos:    Humitas  (Comida,  $1.50,  stock  15)  y  Jugo  de  tomate  (Bebida,
    $1.50,  stock  20)
-    Usuarios:    Danny  Betancourt  (1101234567)  y  Carlos  Pérez  (1107654321)

En  ejecuciones  posteriores  estos  datos  ya  están  guardados  y  se  recuperan  desde
los  archivos,  sin  volver  a  cargarse.

##  Estructura  del  proyecto
restaurante_app/
├──  datos/
│      ├──  productos.json
│      ├──  usuarios.json
│      └──  ventas.json
├──  modelos/
│      ├──  __init__.py
│      ├──  producto.py
│      ├──  usuario.py
│      └──  venta.py
├──  servicios/
│      ├──  __init__.py
│      ├──  archivo_servicio.py
│      └──  restaurante.py
└──  main.py


##  Responsabilidad  de  cada  parte

-    `Producto`  :  código,  nombre,  categoría,  precio,  disponibilidad  y  stock.
    Valida  sus  propios  datos  y  tiene  `to_dict()`  /  `from_dict()`  para  guardarse
    en  JSON.
-    `Usuario`  :  identificación,  nombre  y  correo.  También  valida  sus  datos  y
    se  persiste  en  JSON.
-    `Venta`  :  relaciona  un  usuario  con  un  producto  y  una  cantidad.  No  maneja
    factura,  IVA  ni  pagos.
-    `Restaurante`  :  contiene  toda  la  lógica  de  negocio  (registrar,  buscar,
    actualizar,  eliminar,  vender,  consultar  ventas).  Es  donde  se  aplicó  la
    mejora  de  esta  semana.
-    `ArchivoServicio`  :  lee  y  escribe  los  tres  archivos  JSON  usando
    `with  open()`,  `json.load()`  y  `json.dump()`.
-    `main.py`  :  menú  por  consola.  No  accede  directamente  a  las  listas  del
    servicio,  solo  llama  a  sus  métodos.

##  Mejora  de  la  Semana  12:  índices  con  diccionario

Antes,  buscar  un  producto  por  código  o  un  usuario  por  identificación
implicaba  recorrer  la  lista  completa  comparando  uno  por  uno.  Con  pocos
registros  no  se  nota,  pero  si  la  lista  crece  esa  búsqueda  se  vuelve  más  lenta.

Para  evitar  eso,  `Restaurante`  mantiene,  además  de  las  listas
(`_productos`,  `_usuarios`,  `_ventas`),  tres  diccionarios  que  funcionan  como
índice:

    Diccionario      Clave  →  valor      Para  qué  sirve    
    
    `_indice_productos`      código  de  producto  →  Producto      `buscar_producto()`,  `actualizar_producto()`,  `eliminar_producto()`    
    `_indice_usuarios`      identificación  de  usuario  →  Usuario      `buscar_usuario()`    
    `_ventas_por_usuario`      identificación  de  usuario  →  lista  de  sus  Venta      `consultar_ventas_usuario()`    

Con  esto,  esas  búsquedas  ya  no  recorren  la  lista  completa:  se  resuelven
directamente  con  el  diccionario.  `consultar_ventas_usuario()`  en  particular
solo  devuelve  la  lista  de  ventas  ya  agrupada  de  ese  usuario,  sin  comparar
`usuario_id`  contra  todas  las  ventas  registradas.

Las  listas  se  mantienen  igual  que  antes  porque  siguen  haciendo  falta  para
listar  todo,  calcular  las  categorías  y  guardar  la  información  completa  en
JSON.

Los  diccionarios  se  actualizan  en  el  mismo  momento  en  que  se  registra,
actualiza  o  elimina  algo,  para  que  no  queden  desincronizados  con  la  lista.  Y
al  iniciar  el  programa,  cuando  se  cargan  productos,  usuarios  y  ventas  desde
JSON,  esos  mismos  métodos  de  registro  reconstruyen  los  índices  desde  cero.

El  `set`  que  ya  se  usaba  en  `obtener_categorias()`  (para  mostrar  las
categorías  sin  repetir)  se  mantuvo  igual,  no  se  agregaron  sets  nuevos  porque
no  había  otra  validación  de  unicidad  que  lo  necesitara.

##  Relación  Usuario  +  Producto  →  Venta

  
Usuario  registrado
                ↓
Producto  existente
                ↓
Validar  cantidad
                ↓
Validar  stock  disponible
                ↓
Crear  Venta(...)
                ↓
Agregar  a  la  colección  de  ventas
                ↓
Disminuir  stock  del  producto
                ↓
Guardar  ventas.json  y  productos.json
  

`vender_producto(codigo_producto,  identificacion_usuario,  cantidad)`  busca
usuario  y  producto  por  sus  índices,  valida  cantidad  y  stock,  y  si  todo  está
bien  crea  la  `Venta`,  la  agrega  a  la  colección  (y  al  índice  por  usuario)  y
descuenta  el  stock  del  producto.

##  Persistencia

-  `productos.json`  se  guarda  al  registrar,  actualizar,  eliminar  un  producto  o
    al  realizar  una  venta  (porque  cambia  el  stock).
-  `usuarios.json`  se  guarda  al  registrar  un  usuario.
-  `ventas.json`  se  guarda  al  registrar  una  venta.

##  Manejo  de  excepciones

-  `FileNotFoundError`:  si  algún  JSON  no  existe  todavía,  se  avisa  y  se  inicia
    con  esa  colección  vacía.
-  `json.JSONDecodeError`:  si  el  contenido  no  es  JSON  válido,  se  avisa  y  se
    continúa  con  una  colección  vacía.
-  `PermissionError`:  se  controla  tanto  al  leer  como  al  escribir.
-  `KeyError`:  si  un  registro  del  JSON  no  tiene  alguna  clave  esperada,  se
    omite  solo  ese  registro  y  se  sigue  con  los  demás.
-  `ValueError`:  para  las  validaciones  de  `Producto`,  `Usuario`  y  `Venta`
    (precio  o  stock  negativo,  cantidad  menor  o  igual  a  cero,  campos  vacíos).

No  se  usa  `except:  pass`  en  ningún  punto  del  código.

##  Pruebas  realizadas

1.  Se  ejecutó  `main.py`  sin  archivos  JSON:  cargó  las  tres  colecciones  vacías
      y  sembró  los  datos  de  ejemplo.
2.  Búsqueda  de  un  producto  por  código:  correcta.
3.  Búsqueda  de  un  usuario  por  identificación:  correcta.
4.  Consulta  de  ventas  de  un  usuario  sin  ventas:  devolvió  lista  vacía.
5.  Venta  de  3  unidades:  el  stock  bajó  de  15  a  12  y  quedó  registrada  en
      `ventas.json`.
6.  Consulta  de  ventas  del  mismo  usuario:  mostró  la  venta  anterior.
7.  Se  cerró  y  volvió  a  abrir  el  programa:  productos,  usuarios  y  ventas  se
      recuperaron  desde  los  archivos  y  las  búsquedas  siguieron  funcionando  bien,
      lo  que  confirma  que  los  índices  se  reconstruyeron  correctamente.
8.  Se  intentó  vender  una  cantidad  mayor  al  stock  disponible:  la  venta  fue
      rechazada  y  el  stock  no  cambió.

##  Cómo  ejecutar

1.  Tener  Python  3.9  o  superior.
2.  Ubicarse  en  la  carpeta  `restaurante_app`.
3.  Ejecutar:

  bash
python3  main.py
  