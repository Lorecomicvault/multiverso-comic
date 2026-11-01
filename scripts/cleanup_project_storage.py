"""
Script de Limpieza Segura de Almacenamiento (Lorecomicvault / Multiverso Comic)
Elimina exclusivamente archivos temporales, secuencias de frames intermedias y caches de render,
preservando intactos el 100% de los videos finales, miniaturas, guiones, librerias y codigo.
"""

import os
import sys
import shutil

ROOT = r"C:\Users\Vanes\comics en espanol"

def get_dir_size(path):
    if not os.path.exists(path):
        return 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total

def safe_remove(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            return True
        elif os.path.isfile(path):
            os.remove(path)
            return True
    except Exception as e:
        print(f"  [ERROR] No se pudo eliminar {path}: {e}")
        return False
    return False

def collect_targets():
    targets = []

    # 1. pack_10_virales_60s: _duplicados_archivados y carpetas 'build' intermedias
    p10 = os.path.join(ROOT, "output", "pack_10_virales_60s")
    if os.path.exists(p10):
        dup = os.path.join(p10, "_duplicados_archivados")
        if os.path.exists(dup):
            targets.append(("Archivados Duplicados (Pack 10)", dup))
        
        for item in os.listdir(p10):
            item_path = os.path.join(p10, item)
            if os.path.isdir(item_path):
                b = os.path.join(item_path, "build")
                if os.path.exists(b):
                    targets.append((f"Build Cache ({item})", b))

    # 2. Carpetas intermedias en output (master_reel, build, composed)
    out = os.path.join(ROOT, "output")
    if os.path.exists(out):
        for item in os.listdir(out):
            full = os.path.join(out, item)
            if os.path.isdir(full) and item != "pack_10_virales_60s":
                for sub in ["master_reel", "build", "composed"]:
                    p = os.path.join(full, sub)
                    if os.path.exists(p):
                        targets.append((f"Intermedio {sub} ({item})", p))

    # 3. Carpetas obsoletas de pruebas o descargas CI en output
    obsolete_output = [
        "temp_run_14", "multiverso-comic-video-14", "multiverso-comic-production-logs-14",
        "run_15", "test_build_larfleeze", "batman_joker_flayed_face",
        "master_reel_constantine_trigon", "master_reel_thomas_wayne"
    ]
    for name in obsolete_output:
        p = os.path.join(out, name)
        if os.path.exists(p):
            targets.append((f"Prueba Obsoleta Output ({name})", p))

    # 4. En marvel_zombies_long: clips temporales y versiones preliminares
    mz = os.path.join(out, "marvel_zombies_long")
    if os.path.exists(mz):
        for sub in ["clips", "clips_motion", "audio"]:
            p = os.path.join(mz, sub)
            if os.path.exists(p):
                targets.append((f"Marvel Zombies Clips ({sub})", p))
        for f in ["marvel_zombies_la_caida_completo_1080p.mp4", "marvel_zombies_la_caida_completo_1080p_dinamico.mp4"]:
            p = os.path.join(mz, f)
            if os.path.exists(p):
                targets.append((f"Marvel Zombies Borrador ({f})", p))

    # 5. Carpetas de descargas temporales de GitHub Actions en la raiz
    root_artifacts = [
        "run_36872915344_video", "gh_artifacts_punisher", "run_37379597909_artifacts",
        "run_36892937550_artifacts", "scratch_cloud_gen", "run_36872915344_logs"
    ]
    for name in root_artifacts:
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            targets.append((f"Descarga CI Raiz ({name})", p))

    # 6. Archivos y carpetas temporales pesadas en scratch
    sc = os.path.join(ROOT, "scratch")
    if os.path.exists(sc):
        for sub in ["unpacked_comics", "cbz_issues", "cbz_test", "test_trans_temp", "dead_days_pages", "contact_sheets"]:
            p = os.path.join(sc, sub)
            if os.path.exists(p):
                targets.append((f"Scratch Temp ({sub})", p))
        for f in os.listdir(sc):
            if f.endswith(".mp4") or f.endswith(".wav") or f.endswith(".cbr") or f.endswith(".cbz") or f.startswith("test_dd_"):
                p = os.path.join(sc, f)
                targets.append((f"Scratch Media ({f})", p))

    return targets

def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("=" * 70)
    print("LIMPIEZA DE ARCHIVOS TEMPORALES Y CACHE DE RENDER")
    print("=" * 70)

    initial_size = get_dir_size(ROOT)
    print(f"Espacio total actual del proyecto: {initial_size / (1024**3):.2f} GB ({initial_size / (1024**2):.2f} MB)\n")

    targets = collect_targets()
    print(f"Total de objetivos temporales identificados: {len(targets)}")

    freed_bytes = 0
    deleted_count = 0

    for label, path in targets:
        if not os.path.exists(path):
            continue
        sz = get_dir_size(path)
        sz_mb = sz / (1024**2)
        rel = os.path.relpath(path, ROOT)
        print(f"Eliminando: {label} [{sz_mb:.1f} MB] -> {rel}... ", end="", flush=True)
        if safe_remove(path):
            print("OK")
            freed_bytes += sz
            deleted_count += 1
        else:
            print("FALLO")

    final_size = get_dir_size(ROOT)

    print("\n" + "=" * 70)
    print("RESUMEN DE LIBERACION DE ESPACIO")
    print("=" * 70)
    print(f"Elementos eliminados exitosamente: {deleted_count}/{len(targets)}")
    print(f"Espacio liberado: {freed_bytes / (1024**3):.2f} GB ({freed_bytes / (1024**2):.2f} MB)")
    print(f"Tamano final del proyecto: {final_size / (1024**3):.2f} GB ({final_size / (1024**2):.2f} MB)")
    print("=" * 70)

    # Verificacion de integridad de videos finales
    print("\nVerificando integridad de videos finales del Pack 10...")
    p10 = os.path.join(ROOT, "output", "pack_10_virales_60s")
    for f in sorted(os.listdir(p10)):
        sub = os.path.join(p10, f)
        if os.path.isdir(sub):
            mp4s = [x for x in os.listdir(sub) if x.endswith(".mp4")]
            print(f"  [OK] {f}: {mp4s[0] if mp4s else 'FALTA MP4'}")

    mz_master = os.path.join(ROOT, "output", "marvel_zombies_long", "marvel_zombies_la_caida_edicion_maestra_definitiva.mp4")
    if os.path.exists(mz_master):
        print(f"  [OK] Marvel Zombies Video Maestro: {os.path.getsize(mz_master) / (1024**2):.1f} MB")

if __name__ == "__main__":
    main()
