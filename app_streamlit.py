import streamlit as st
import requests

# URL da API Flask
API_URL = "http://127.0.0.1:5000/prever"

# Categorias de seletores
make_categories = [
    "ACURA", "ALFA ROMEO", "ASTON MARTIN", "AUDI", "BENTLEY", "BMW", "BUGATTI",
    "BUICK", "CADILLAC", "CHEVROLET", "CHRYSLER", "DODGE", "FIAT", "FORD",
    "GENESIS", "GMC", "HONDA", "HYUNDAI", "INFINITI", "JAGUAR", "JEEP", "KIA",
    "LAMBORGHINI", "LAND ROVER", "LEXUS", "LINCOLN", "MASERATI", "MAZDA",
    "MERCEDES-BENZ", "MINI", "MITSUBISHI", "NISSAN", "PORSCHE", "RAM",
    "ROLLS-ROYCE", "SCION", "SMART", "SRT", "SUBARU", "TOYOTA", "VOLKSWAGEN", "VOLVO"
]
vehicle_class_categories = [
    "COMPACT", "FULL-SIZE", "MID-SIZE", "MINICOMPACT", "MINIVAN",
    "PICKUP TRUCK - SMALL", "PICKUP TRUCK - STANDARD",
    "SPECIAL PURPOSE VEHICLE", "STATION WAGON - MID-SIZE",
    "STATION WAGON - SMALL", "SUBCOMPACT", "SUV - SMALL", "SUV - STANDARD",
    "TWO-SEATER", "VAN - CARGO", "VAN - PASSENGER"
]
transmission_categories = [
    "A10", "A4", "A5", "A6", "A7", "A8", "A9", "AM5", "AM6", "AM7", "AM8", "AM9",
    "AS10", "AS4", "AS5", "AS6", "AS7", "AS8", "AS9", "AV", "AV10", "AV6", "AV7",
    "AV8", "M5", "M6", "M7"
]
fuel_type_categories = [
    "Diesel", "Ethanol (E85)", "Premium Gasoline", "Regular Gasoline"
]


# Título
st.title("Calculadora de Consumo de Combustível 🚗")

# Subtítulo
st.subheader("Preencha os dados abaixo e descubra mais precisamente quanto seu carro emite de Co2:")

# Formulário para entrada de dados
with st.form("prediction_form"):
    st.markdown("### Dados do Motor e Consumo")
    engine_size = st.number_input(
        "Tamanho do Motor (L):",
        min_value=0.0,
        format="%.1f",
        step=0.1,
        help="Indique o tamanho do motor em litros. Por exemplo: 3.5.",
    )
    cylinders = st.number_input(
        "Número de Cilindros:",
        min_value=1,
        format="%d",
        help="Informe a quantidade de cilindros no motor. Por exemplo: 6.",
    )
    fuel_city = st.number_input(
        "Consumo de Combustível na Cidade (L/100 km):",
        min_value=0.0,
        format="%.1f",
        step=0.1,
        help="Consumo médio do veículo na cidade em litros por 100 km percorridos.",
    )
    fuel_hwy = st.number_input(
        "Consumo de Combustível na Estrada (L/100 km):",
        min_value=0.0,
        format="%.1f",
        step=0.1,
        help="Consumo médio do veículo na estrada em litros por 100 km percorridos.",
    )
    fuel_comb = st.number_input(
        "Consumo Médio Combinado (L/100 km):",
        min_value=0.0,
        format="%.1f",
        step=0.1,
        help="Consumo médio combinado do veículo em litros por 100 km.",
    )
    fuel_mpg = st.number_input(
        "Consumo Médio Combinado (mpg):",
        min_value=0.0,
        format="%.1f",
        step=0.1,
        help="Consumo médio combinado em milhas por galão.",
    )

    st.markdown("### Informações do Veículo")
    # Campo para selecionar a marca
    make = st.selectbox(
        "Marca (Fabricante):",
        options=make_categories,
        help="Selecione a marca do veículo.",
    )
    # Campo para selecionar a classe do veículo
    vehicle_class = st.selectbox(
        "Classe do Veículo:",
        options=vehicle_class_categories,
        help="Selecione a classe do veículo. Por exemplo: Compacto ou SUV.",
    )
    # Campo de entrada para o modelo
    model = st.text_input(
        "Modelo do Veículo:",
        help="Informe o modelo exato do veículo. Por exemplo: Civic, Corolla.",
    )
    # Campo para selecionar o tipo de transmissão
    st.markdown("""##### Informações da Transmissão
        A: Automático (ex: A6 = 6 marchas)
    AM: Automatizado manual (ex: AM6 = 6 marchas)
    AS: Automático com troca manual (ex: AS6 = 6 marchas)
    AV: Transmissão continuamente variável (CVT) (ex: AV6 = 6 marchas simuladas)
    M: Manual (ex: M6 = 6 marchas)""")
    transmission = st.selectbox(
        "Tipo de Transmissão:",
        options=transmission_categories,
        help="Selecione o tipo de transmissão. Por exemplo: A6 (Automática de 6 marchas).",
    )
    # Campo para selecionar o tipo de combustível
    fuel_type = st.selectbox(
        "Tipo de Combustível:",
        options=fuel_type_categories,
        help="Selecione o tipo de combustível. Por exemplo: Diesel.",
    )

    # Botão para submeter o formulário
    submitted = st.form_submit_button("Enviar")

# Quando o formulário é enviado
if submitted:
    # Dados no formato JSON
    input_data = {
        "Engine Size(L)": engine_size,
        "Cylinders": cylinders,
        "Fuel Consumption City (L/100 km)": fuel_city,
        "Fuel Consumption Hwy (L/100 km)": fuel_hwy,
        "Fuel Consumption Comb (L/100 km)": fuel_comb,
        "Fuel Consumption Comb (mpg)": fuel_mpg,
        "Make": make,
        "Vehicle Class": vehicle_class,
        "Model": model,
        "Transmission": transmission,
        "Fuel Type": fuel_type,
    }

    #st.json(input_data)  # Exibir os dados enviados no formato JSON

    try:
        # Enviar os dados para a API Flask
        response = requests.post(API_URL, json=input_data)
        response_data = response.json()

        # Exibir o resultado da previsão
        if response.status_code == 200:
            prediction = response_data["prediction"][0]
            st.success(f"Previsão: {prediction:.2f} gramas de Co2 por quilômetro rodado! 🫨")
        else:
            st.error(f"Erro na API: {response_data.get('erro', 'Erro desconhecido')}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")




