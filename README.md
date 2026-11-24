# Shell diésel más barata de camino

Página para el móvil: con un destino, lista las gasolineras Shell más convenientes cerca de la ruta (sin Shell Express);
sin destino, las de alrededor. Diésel normal o Diésel premium.

Cada gasolinera muestra:
- el precio por litro, el horario y la dirección;
- la distancia y el tiempo reales por carretera desde la salida;
- cuántos km y minutos añade el desvío;
- lo que cuesta llenar (según el combustible que queda y el depósito);
- el coste real total (llenar + el combustible del desvío), por el que se ordenan;
- los botones «Copiar dirección» e «Ir con Waze».

## Modo coche (Copiloto de voz)

Cuando el coche avisa de combustible bajo, la app *Copiloto de voz* (46Wen/apps) manda un aviso al iPhone (ntfy). Al
tocarlo se abre esta página así:

    https://46wen.github.io/shell-diesel/?auto=1&km=<autonomía>#car=<litros>,<l/100km>,<hora>,<ahora>

Con los litros y el consumo del coche, busca alrededor de su ubicación (el «radio cercano» de *Más ajustes*), se queda
con las Shell abiertas cuando llegue y a menos de la mitad de la autonomía por carretera, elige la más barata (llenar +
trayecto) y abre Waze hacia ella. Si no hay ninguna tan cerca, elige la más cercana abierta, para llegar seguro. Debajo
queda la lista, por si prefiere otra.

iOS solo deja que una página abra otra app con su propia pregunta: aparece «¿Abrir en Waze?» y basta con tocar
*Abrir*. Para no tener que dar permiso de ubicación cada vez: Ajustes → Apps → Safari → Ubicación → Permitir.

## Datos

- Precios: datos abiertos del Geoportal de Gasolineras del Ministerio de Industria (precios oficiales, sin el
  descuento ClubSmart). `.github/workflows/update.yml` ejecuta `scripts/update.py` cada hora: se queda solo con las
  Shell y las guarda en `data/shell.json`.
- Búsqueda de direcciones: OpenStreetMap Nominatim.
- Rutas, distancias y tiempos: el servicio público de OSRM.

## Publicación

GitHub Pages: Settings → Pages → Source «Deploy from a branch», rama `main`, carpeta `/ (root)`.
La dirección es `https://<usuario>.github.io/shell-diesel/`. En el iPhone, ábrala en Safari → Compartir → «Añadir a
pantalla de inicio».
