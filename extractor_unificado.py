def actualizar_json_historico(nuevos_eventos: List[dict], ruta_json: str = "eventos.json") -> List[dict]:
    archivo = Path(ruta_json)
    existentes = []
    if archivo.exists():
        existentes = json.loads(archivo.read_text(encoding="utf-8"))

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    # Conservamos solo los eventos cuya fecha sea hoy o futura
    vigentes = [ev for ev in existentes if ev.get("fecha", "") >= fecha_hoy]

    vistos = {(ev["titulo"].strip().lower(), ev["fecha"]) for ev in vigentes}
    combinados = list(vigentes)

    agregados = 0
    for ev in nuevos_eventos:
        if ev.get("fecha", "") < fecha_hoy:
            continue
        clave = (ev["titulo"].strip().lower(), ev["fecha"])
        if clave not in vistos:
            vistos.add(clave)
            combinados.append(ev)
            agregados += 1

    combinados.sort(key=lambda e: e["fecha"])
    for idx, ev in enumerate(combinados, start=1):
        ev["id"] = idx

    archivo.write_text(json.dumps(combinados, ensure_ascii=False, indent=4), encoding="utf-8")
    print(f"[OK] Se agregaron {agregados} eventos nuevos y se limpiaron los vencidos. Total vigentes: {len(combinados)}.")
    return combinados
