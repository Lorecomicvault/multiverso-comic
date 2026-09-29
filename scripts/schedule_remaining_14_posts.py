"""
Script de Programación Masiva y Progresiva de Viñetas de Cómics Originales en Facebook
Meta Graph API - Programación Nativa de 3 Posts por Día (Total 19 Publicaciones)
"""

import os
import sys
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
sys.path.append(r'C:\Users\Vanes\comics en espanol')
from src.facebook_photo_publisher import publish_facebook_photo

# Zona horaria Bogotá / Colombia (UTC-5)
TZ_LOCAL = datetime.timezone(datetime.timedelta(hours=-5))

def get_timestamp(year, month, day, hour, minute):
    dt = datetime.datetime(year, month, day, hour, minute, 0, tzinfo=TZ_LOCAL)
    return int(dt.timestamp())

POSTS_TO_SCHEDULE = [
    # --- DÍA 2: Miércoles 30 Sep 2026 (Completar con el post de la mañana) ---
    {
        "slot": "Día 2 - Miércoles 30 Sep 08:30 AM",
        "timestamp": get_timestamp(2026, 9, 30, 8, 30),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_04_flash_crisis.jpg",
        "caption": """⚡ "TIENE QUE HABER UNA ESPERANZA... SIEMPRE LA HAY." (1985)

En Crisis en Tierras Infinitas #8, el Antimonitor estaba a instantes de disparar su cañón de antimateria para borrar todo el multiverso. Barry Allen tomó la decisión más dura: corrió más rápido de lo que cualquier ser vivo jamás lo había hecho, rompiendo la barrera temporal y desintegrando su propio cuerpo átomo por átomo para destruir el núcleo del cañón.

Durante más de 23 años editoriales, su partida fue respetada como definitiva y trascendental. No hubo trucos inmediatos: Barry Allen se consagró como el máximo símbolo del sacrificio desinteresado en la historia de DC.

¿Consideras este el momento heroico más grande de DC, o cuál otro crees que lo supera? 👇⚡

#TheFlash #BarryAllen #CrisisOnInfiniteEarths #DCComics #MultiversoComic #ComicsEnEspañol #Comics"""
    },

    # --- DÍA 3: Jueves 1 Oct 2026 (3 Posts) ---
    {
        "slot": "Día 3 - Jueves 1 Oct 08:30 AM",
        "timestamp": get_timestamp(2026, 10, 1, 8, 30),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_07_cap_hail_hydra.jpg",
        "caption": """🛡️ LAS DOS PALABRAS QUE PARALIZARON AL MUNDO DE LOS CÓMICS (2016)

En mayo de 2016, Nick Spencer y Jesús Saiz lanzaron Captain America: Steve Rogers #1. Tras arrojar a Jack Flag al vacío de un avión en pleno vuelo, el símbolo viviente de la libertad miró a la cámara y susurró: "HAIL HYDRA."

El impacto cultural fue tan colosal que llegó a los noticieros internacionales antes de revelarse la manipulación de la realidad provocada por Kobik y el Cubo Cósmico. Pocas veces una última viñeta ha generado tanta intriga y debate en la era moderna.

¿Cuál fue tu reacción la primera vez que leíste esta página? ¿Te lo viste venir o te tomó completamente por sorpresa? 👇🔥

#CaptainAmerica #HailHydra #SteveRogers #Marvel #MarvelComics #MultiversoComic #ComicsEnEspañol"""
    },
    {
        "slot": "Día 3 - Jueves 1 Oct 01:00 PM",
        "timestamp": get_timestamp(2026, 10, 1, 13, 0),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_08_ghost_rider_hulk.jpg",
        "caption": """🔥 CUANDO EL JUEZ DEL INFIERNO ABSOLVIÓ A HULK (2007)

Durante los eventos de World War Hulk, Johnny Blaze desató al Motorista Fantasma para detener la invasión de Hulk en Nueva York. Tras un enfrentamiento devastador, Zarathos tomó el control total del espíritu de venganza y contempló el alma del gigante esmeralda.

Lo que descubrió dejó perplejos a los Vengadores: la Mirada de Penitencia no condenó a Hulk. Zarathos reconoció que Hulk y sus Warbound buscaban justicia legítima tras la destrucción de su hogar en Sakaar, y que los verdaderos culpables eran los Illuminati. El demonio simplemente dio media vuelta y abandonó la ciudad.

¿Crees que la furia de Hulk contra los Illuminati estaba 100% justificada? ¡Te leemos en los comentarios! 👇💥

#WorldWarHulk #Hulk #GhostRider #Marvel #MarvelComics #MultiversoComic #ComicsEnEspañol"""
    },
    {
        "slot": "Día 3 - Jueves 1 Oct 07:30 PM",
        "timestamp": get_timestamp(2026, 10, 1, 19, 30),
        "image": r"C:\Users\Vanes\comics en espanol\output\batman_red_death_speed_force\scene_03\scene_03.jpg",
        "caption": """🦇⚡ EL BATMAN QUE ROBÓ LA SPEED FORCE (2017)

En el Multiverso Oscuro (Tierra -52), un Bruce Wayne envejecido vio caer a todos sus aliados ante el crimen imparable de Gotham. Desesperado por el poder absoluto para salvar a su mundo, Bruce sometió a Barry Allen y lo encadenó al frente del Batmóvil cósmico modificado con los motores de la Cinta Cósmica.

"¡No puedes entrar a la Speed Force de esta manera! ¡Nos desgarrará a los dos!", gritaba Barry.
"Lo sé... pero ahora salvaremos el mundo juntos", respondió Bruce, antes de que el rayo los fusionara en una sola entidad implacable: Red Death.

¿Es The Red Death la versión oscura de Batman más letal del Multiverso Oscuro? 👇💀

#Batman #TheRedDeath #DarkNightsMetal #Flash #DCComics #MultiversoComic #ComicsEnEspañol"""
    },

    # --- DÍA 4: Viernes 2 Oct 2026 (3 Posts) ---
    {
        "slot": "Día 4 - Viernes 2 Oct 08:30 AM",
        "timestamp": get_timestamp(2026, 10, 2, 8, 30),
        "image": r"C:\Users\Vanes\comics en espanol\output\daredevil_shadowland_bullseye\scene_03\scene_03.jpg",
        "caption": """😈 CUANDO DAREDEVIL PERDIÓ SU ALMA EN LA OSCURIDAD (2010)

En Shadowland #1, Matt Murdock asumió el liderazgo del clan de La Mano con la intención de usar su ejército para proteger la Cocina del Infierno. Pero cuando Bullseye regresó para desafiarlo en su propia fortaleza, el código moral inquebrantable del Hombre Sin Miedo llegó a su fin.

Ante la mirada atónita de Luke Cage y Puño de Hierro, Murdock replicó el mismo acto con el que Bullseye arrebató la vida de Elektra años atrás, cruzando el límite que ningún héroe de Hell's Kitchen creyó que cruzaría jamás.

¿Consideras que Bullseye merecía ese desenlace o Daredevil cometió el mayor error de su carrera? 👇⚖️

#Daredevil #Bullseye #Shadowland #MarvelComics #Marvel #MultiversoComic #ComicsEnEspañol"""
    },
    {
        "slot": "Día 4 - Viernes 2 Oct 01:00 PM",
        "timestamp": get_timestamp(2026, 10, 2, 13, 0),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_11_black_adam_ww3.jpg",
        "caption": """⚡ EL DÍA EN QUE UN SOLO HOMBRE ENFRENTÓ A TODOS LOS HÉROES (2007)

En World War III (evento de la serie semanal 52), la pérdida devastadora de su familia desató una furia incontrolable en Black Adam. Durante semanas, Teth-Adam avanzó por todo el globo terráqueo derribando ejércitos enteros, la Patrulla Condenada, los Jóvenes Titanes y la Sociedad de la Justicia.

Hicieron falta los esfuerzos coordinados de toda la comunidad sobrehumana del planeta y una estratagema mística para cambiar su palabra mágica y poder contenerlo. Una demostración histórica de la escala colosal de poder que posee Black Adam cuando no contiene sus golpes.

¿Quién crees que ganaría en un mano a mano sin límites: Black Adam o Superman enfurecido? 👇⚡

#BlackAdam #DCComics #WorldWarIII #JSA #JusticeLeague #MultiversoComic #ComicsEnEspañol"""
    },
    {
        "slot": "Día 4 - Viernes 2 Oct 07:30 PM",
        "timestamp": get_timestamp(2026, 10, 2, 19, 30),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_12_tower_babel_ras.jpg",
        "caption": """🧠 LA PARANOIA DE BATMAN PUSO EN JAQUE A LA LIGA DE LA JUSTICIA (2000)

En JLA: Tower of Babel (Mark Waid y Howard Porter), Ra's al Ghul dio el golpe maestro más humillante a la Liga de la Justicia. No utilizó tecnología alienígena ni magia ancestral: robó los protocolos secretos de contingencia que el mismísimo Batman había diseñado meticulosamente para neutralizar a cada uno de sus compañeros de equipo.

Kryptonita sintética para Superman, vibraciones para Flash, gas del miedo para Linterna Verde, hidrofobia para Aquaman. La desconfianza de Bruce Wayne fracturó la confianza del equipo para siempre y desembocó en su expulsión de la Liga.

¿Hizo bien Batman en diseñar planes para someter a sus amigos por si caían en el mal, o fue una traición imperdonable? 👇🦇

#Batman #TowerOfBabel #JusticeLeague #JLA #DCComics #MultiversoComic #ComicsEnEspañol"""
    },

    # --- DÍA 5: Sábado 3 Oct 2026 (3 Posts) ---
    {
        "slot": "Día 5 - Sábado 3 Oct 08:30 AM",
        "timestamp": get_timestamp(2026, 10, 3, 8, 30),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_13_grim_knight.jpg",
        "caption": """💀 EL BATMAN QUE NUNCA TUVO PIEDAD (2019)

¿Qué habría ocurrido si la noche en el Callejón del Crimen, un joven Bruce Wayne recogía la pistola que cayó de las manos de Joe Chill? Esa es la perturbadora premisa de The Grim Knight (Scott Snyder y Eduardo Risso).

En esa retorcida realidad, Batman no se juró jamás usar armas de fuego: las convirtió en su herramienta principal. Gotham se transformó en un estado policial militarizado donde cada criminal fue erradicado con armamento de grado bélico, convirtiéndolo en uno de los aliados más temibles del Batman Que Ríe.

¿Prefieres la regla moral clásica de Batman de no usar armas letales, o esta versión implacable te parece fascinante? 👇🔫

#TheGrimKnight #Batman #DCComics #DarkMultiverse #MultiversoComic #ComicsEnEspañol"""
    },
    {
        "slot": "Día 5 - Sábado 3 Oct 01:00 PM",
        "timestamp": get_timestamp(2026, 10, 3, 13, 0),
        "image": r"C:\Users\Vanes\comics en espanol\scratch_cloud_gen\punisher_kills_marvel_universe\scene_01\scene_01.jpg",
        "caption": """🎯 "ALGUIEN TENÍA QUE SER EL PRIMERO." (1995)

En Punisher Kills the Marvel Universe, Garth Ennis concibió una de las historias 'What If...?' más crudas de los años noventa. Tras perder a su familia en medio de una batalla colateral entre héroes y villanos, Frank Castle no distinguió bandos y emprendió una cacería implacable contra todos los seres con superpoderes de la Tierra.

Con tácticas militares, emboscadas y una determinación inquebrantable, Frank fue tachando nombres legendarios de su lista uno tras otro en una de las lecturas más comentadas de Marvel.

¿Qué personaje crees que resistiría más tiempo si The Punisher decidiera cazarlo metódicamente? 👇💀

#ThePunisher #FrankCastle #Marvel #MarvelComics #MultiversoComic #ComicsEnEspañol"""
    },
    {
        "slot": "Día 5 - Sábado 3 Oct 07:30 PM",
        "timestamp": get_timestamp(2026, 10, 3, 19, 30),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_15_marvel_ruins_banner.jpg",
        "caption": """☢️ LA HISTORIA MÁS CRUDA Y DESOLADORA DE MARVEL (1995)

En 1995, Warren Ellis y Cliff Nielsen crearon Marvel Ruins, la antítesis directa de Marvels de Kurt Busiek y Alex Ross. En este universo, la radiación cósmica y los experimentos de la ciencia no crearon superhéroes majestuosos: desataron tumores, mutaciones grotescas y sufrimiento humano absoluto.

Bruce Banner no se convirtió en un gigante de fuerza indestructible, sino en un ser deformado y agonizante por la radiación gamma. Una obra maestra oscura de culto que exploró las consecuencias realistas y escalofriantes de las leyes de la física.

¿Conocías la historia de Ruins? ¿Consideras que Marvel debería explorar más este tipo de relatos maduros? 👇📚

#MarvelRuins #BruceBanner #Hulk #Marvel #MarvelComics #MultiversoComic #ComicsEnEspañol"""
    },

    # --- DÍA 6: Domingo 4 Oct 2026 (3 Posts) ---
    {
        "slot": "Día 6 - Domingo 4 Oct 08:30 AM",
        "timestamp": get_timestamp(2026, 10, 4, 8, 30),
        "image": r"C:\Users\Vanes\comics en espanol\output\black_manta_infanticidio_aquaman\scene_04\scene_04.jpg",
        "caption": """🌊 EL MOMENTO QUE DEFINIÓ LA RIVALIDAD DE AQUAMAN PARA SIEMPRE (1977)

En Adventure Comics #452 (Death of a Prince), David Michelinie y Jim Aparo cambiaron para siempre el destino de los cómics de DC. Black Manta ejecutó el plan más perverso y despiadado: privó de oxígeno al pequeño Arthur Jr., marcando una de las tragedias más impactantes y solemnes de la Edad de Bronce.

La viñeta de Aquaman cargando a su hijo en brazos simbolizó la transición hacia historias mucho más maduras y profundas, sellando un rencor irreconciliable que dura hasta nuestros días.

¿Es Black Manta el villano más rencoroso e implacable de todo DC Comics? 👇🔱

#Aquaman #BlackManta #DCComics #DeathOfAPrince #MultiversoComic #ComicsEnEspañol"""
    },
    {
        "slot": "Día 6 - Domingo 4 Oct 01:00 PM",
        "timestamp": get_timestamp(2026, 10, 4, 13, 0),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\test_spider.jpg",
        "caption": """🕷️ "CUALQUIERA PUEDE GANAR CUANDO LAS PROBABILIDADES SON FÁCILES..." (1966)

The Amazing Spider-Man #33 por Stan Lee y Steve Ditko ("¡Si este es mi destino...!") es reconocida casi unánimemente como una de las secuencias más inspiradoras jamás impresas en tinta y papel. Atrapado bajo toneladas de maquinaria de acero mientras el agua inunda la guarida y la vida de la tía May pende de un hilo con la medicina al alcance de su mano.

Peter Parker recurre a cada gota de determinación humana, negándose a rendirse ante la derrota. Este panel definió para siempre la esencia inquebrantable de Spider-Man: levantarse cuando no queda ninguna posibilidad lógica de éxito.

¿Es esta la mejor escena en los más de 60 años de historia de Spider-Man? 👇🕸️

#SpiderMan #PeterParker #StanLee #SteveDitko #Marvel #MarvelComics #MultiversoComic #ComicsEnEspañol"""
    },
    {
        "slot": "Día 6 - Domingo 4 Oct 07:30 PM",
        "timestamp": get_timestamp(2026, 10, 4, 19, 30),
        "image": r"C:\Users\Vanes\comics en espanol\output\spiderman_back_in_black_kingpin\scene_04\scene_04.jpg",
        "caption": """🖤 EL DÍA EN QUE SPIDER-MAN SE QUITÓ LA MÁSCARA ANTE KINGPIN (2007)

Tras los sucesos de Civil War, un francotirador contratado por Wilson Fisk hirió gravemente a la tía May. En Back in Black (The Amazing Spider-Man #542 por J. Michael Straczynski), Peter Parker vistió nuevamente su traje negro, caminó hasta la prisión de máxima seguridad de Ryker's Island y se encerró en el patio con Kingpin frente a todos los convictos.

Sin bromas, sin chistes y sin contener su fuerza por primera vez en años, Peter le demostró a Kingpin la diferencia abismal entre un criminal arrogante y un hombre araña dispuesto a todo por defender a su familia.

¿Cuál es tu versión favorita de Peter: el héroe alegre que lanza bromas o el justiciero implacable que no perdona? 👇👊

#SpiderMan #Kingpin #BackInBlack #Marvel #MarvelComics #MultiversoComic #ComicsEnEspañol"""
    },

    # --- DÍA 7: Lunes 5 Oct 2026 (1 Post Final -> 19 de 19) ---
    {
        "slot": "Día 7 - Lunes 5 Oct 08:30 AM",
        "timestamp": get_timestamp(2026, 10, 5, 8, 30),
        "image": r"C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_19_xmen_25_wolverine_magneto.jpg",
        "caption": """🩸 EL DÍA EN QUE MAGNETO CRUZÓ EL LÍMITE CON WOLVERINE (1993)

En X-Men #25 (Atracciones Fatales, por Fabian Nicieza y Andy Kubert), se vivió uno de los clímax más brutales de los años noventa en la estación espacial Avalon. Tras recibir un corte crítico, Magneto utilizó todo el poder de sus campos magnéticos para hacer lo impensable: desgarró el adamantium líquido directamente de los huesos de Wolverine a través de cada poro de su piel.

El impacto fue tan traumático que el profesor Charles Xavier tomó la drástica decisión de apagar la mente de Magneto, un suceso que posteriormente daría nacimiento a la entidad Onslaught.

¿Consideras a Magneto un villano puro o un líder que lucha por la supervivencia de su especie a cualquier costo? 👇🧲

#Wolverine #Magneto #XMen #FatalAttractions #Marvel #MarvelComics #MultiversoComic #ComicsEnEspañol"""
    }
]

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(f"Iniciando programacion de {len(POSTS_TO_SCHEDULE)} posts en Facebook...")

    # Consultar posts ya programados en la página para evitar duplicados
    existing_timestamps = set()
    try:
        token = os.environ.get('FB_PAGE_TOKEN')
        pid = os.environ.get('FB_PAGE_ID', '1289410784257454')
        import requests
        url = f"https://graph.facebook.com/v20.0/{pid}/scheduled_posts?access_token={token}&fields=id,scheduled_publish_time"
        r = requests.get(url, timeout=10).json()
        for p in r.get('data', []):
            st = p.get('scheduled_publish_time')
            if st:
                existing_timestamps.add(int(st))
        print(f"Actualmente hay {len(existing_timestamps)} posts programados en Facebook.")
    except Exception as e:
        print(f"Aviso al consultar posts existentes: {e}")

    scheduled_count = 0
    for idx, post in enumerate(POSTS_TO_SCHEDULE, 1):
        slot = post["slot"]
        ts = post["timestamp"]
        img = post["image"]
        caption = post["caption"]

        print(f"\n[{idx}/{len(POSTS_TO_SCHEDULE)}] Procesando: {slot} (TS: {ts})")
        if ts in existing_timestamps:
            print(f">> Ya programado previamente para este horario. Omitiendo duplicado.")
            scheduled_count += 1
            continue

        if not os.path.exists(img):
            print(f">> ERROR: Imagen no encontrada en: {img}")
            continue

        res = publish_facebook_photo(img, caption, scheduled_timestamp=ts)
        if res.get("success"):
            print(f">> EXITO: Programado con Photo ID: {res.get('id')} | Post ID: {res.get('post_id')}")
            scheduled_count += 1
            existing_timestamps.add(ts)
        else:
            print(f">> ERROR al programar: {res.get('error')}")

    print(f"\n==========================================")
    print(f"Total confirmados en el calendario: {scheduled_count}/{len(POSTS_TO_SCHEDULE)}")
    print(f"==========================================")

if __name__ == '__main__':
    main()
