import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"


def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    #ALERT
    alert = AlertManager(page)


    deposito = DepositoStrumenti(
        "Deposito Strumenti Musicali", "Alessandro Visconti"
    )
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # carica file
    except FileNotFoundError as e:
        alert.show_alert(
            f"❌ {e}"
        )  # mostra l'errore

    #UI ELEMENTI

    # mostra il nome e il responsabile del deposito
    txt_titolo = ft.Text(
        value=deposito.nome, size=38, weight=ft.FontWeight.BOLD
    )
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD,
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(
        value=deposito.get_responsabile(), label="Responsabile"
    )

    # ListView mostra la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(
        expand=True, spacing=5, padding=10, auto_scroll=True
    )

    # per aggiungere un nuovo strumento (tipo, marca, anno, valore in euro)
    tipo_input = ft.TextField(label="Tipo")
    marca_input = ft.TextField(label="Marca")
    anno_input = ft.TextField(label="Anno di acquisto")

    # TextField disabilitato e centratore per il valore in euro
    txt_valore = ft.TextField(
        value="0", width=80, disabled=True, text_align=ft.TextAlign.CENTER
    )

    # FUNZIONI APP
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # HANDLERS APP
    def cambia_tema(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if toggle_cambia_tema.value
            else ft.ThemeMode.LIGHT
        )
        toggle_cambia_tema.label = (
            "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        )
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # per la gestione dell'inserimento di un nuovo strumento
    def aggiungi_strumento(e):
        try:
            anno = int(anno_input.value)
            valore = float(txt_valore.value)

            if not tipo_input.value or not marca_input.value:
                alert.show_alert("❌ Errore: Compilare tutti i campi.")
                return

            deposito.aggiungi_strumento(
                tipo_input.value, marca_input.value, anno, valore
            )

            # reset campi input
            tipo_input.value = ""
            marca_input.value = ""
            anno_input.value = ""
            txt_valore.value = "0"

            aggiorna_lista_strumenti()
        except ValueError:
            alert.show_alert(
                "Errore: inserisci valori numerici validi per anno e valore."
            )

    def incrementa_valore(e):
        current_val = float(txt_valore.value)
        txt_valore.value = f"{int(current_val + 10)}"
        txt_valore.update()

    def decrementa_valore(e):
        current_val = float(txt_valore.value)
        if current_val >= 10:
            txt_valore.value = f"{int(current_val - 10)}"
            txt_valore.update()

    # EVENTI
    toggle_cambia_tema = ft.Switch(
        label="Tema scuro", value=True, on_change=cambia_tema
    )
    pulsante_conferma_responsabile = ft.ElevatedButton(
        "Conferma", on_click=conferma_responsabile
    )

    # pulsanti per l'inserimento di uno strumento e per il contatore del valore
    pulsante_aggiungi_strumento = ft.ElevatedButton(
        "Aggiungi strumento", on_click=aggiungi_strumento
    )
    pulsante_incrementa_valore = ft.IconButton(
        icon=ft.Icons.ADD, icon_color="green", on_click=incrementa_valore
    )
    pulsante_decrementa_valore = ft.IconButton(
        icon=ft.Icons.REMOVE, icon_color="red", on_click=decrementa_valore
    )

    # LAYOUT
    page.add(
        toggle_cambia_tema,
        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),
        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(
            spacing=200,
            controls=[input_responsabile, pulsante_conferma_responsabile],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(
            spacing=30,
            controls=[
                tipo_input,
                marca_input,
                anno_input,
                ft.Row(
                    [
                        pulsante_decrementa_valore,
                        txt_valore,
                        pulsante_incrementa_valore,
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        pulsante_aggiungi_strumento,
        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()


ft.app(target=main)