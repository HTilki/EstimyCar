import streamlit as st


def accueil():
    """
    Fonction pour afficher la page d'accueil de l'application Streamlit.

    ## Affichage

        - Un titre de bienvenue.
        - Une description de l'application.
        - Des informations sur les deux onglets disponibles, Acheteur et Vendeur.
        - Un message d'information sur l'origine des données extraites de La Centrale.
        - Un pied de page fixé en bas de la page avec les liens vers les profils GitHub des créateurs.

    """

    st.markdown(
        "<p style='font-size: 30px; text-align: center;'><em>Bienvenue sur notre application Streamlit</em></p>",
        unsafe_allow_html=True,
    )
    st.markdown(" ")
    st.markdown(
        "<p style='color: #C41E3A;'; font-size: 18px;><strong>Cette application est une alternative aux estimateurs de valeurs de véhicule sans pour autant demander vos données personnelles !</strong></p>",
        unsafe_allow_html=True,
    )
    st.markdown(" ")
    st.markdown(
        "<p style='font-size: 17px'>Vous trouverez 2 onglets :</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size: 17px'>- L'onglet <strong>Acheteur</strong> 🔍🚗 : qui va vous permettre de trouver la voiture de vos rêves en fonction des caractéristiques que vous aurez choisi. ✨</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size: 17px'>- L'onglet <strong>Vendeur</strong> 💵📈: découvrez le pouvoir d'estimer le juste prix de votre voiture <strong>gratuitement</strong> en fonction des caractéristiques à votre disposition. 😎</p>",
        unsafe_allow_html=True,
    )

    nombre_espaces = 5
    for _ in range(nombre_espaces):
        st.markdown(" ")

    info_content = """
    Les données ont été extraites depuis [**La Centrale**](https://www.lacentrale.fr/).

    Ces données sont exclusivement utilisées à des fins pédagogiques, dans le cadre de l’enseignement et de la recherche. Toute utilisation à des fins commerciales est strictement interdite.
    """

    st.info(info_content, icon="ℹ️")

    footer_html = """
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; padding: 10px; text-align: center;margin-left: 160px">
        Créé par <a href="https://github.com/aybuke-b">Aybuké BICAT</a> et <a href="https://github.com/HTilki">Hassan TILKI</a>
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)
