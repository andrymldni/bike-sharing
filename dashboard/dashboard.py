import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load the processed data
day_df = pd.read_csv('dashboard/day_df.csv')
hour_df = pd.read_csv('dashboard/hour_df.csv')

# Sidebar
st.sidebar.title('Bike Sharing Analysis')
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-vector/couple-bicycle-concept-illustration_114360-4629.jpg?w=740&t=st=1701444903~exp=1701445503~hmac=aacf8226db552670e94d0d50358e80f806836922054e9aadd667b046bb25d0bb")
    # Sidebar
    st.sidebar.title("Data Overview")
    selected_dataset = st.sidebar.radio("Pilih dataset yang ingin ditampilkan", ["Day Dataset", "Hour Dataset"])

    # Data Wrangling
    if selected_dataset == "Day Dataset":
        st.header("Day Dataset")
        st.dataframe(day_df.head())
    else:
        st.header("Hour Dataset")
        st.dataframe(hour_df.head())

# Assessing Data
st.header("Assessing Data")

if selected_dataset == "Day Dataset":
    st.subheader("Duplicate Check")
    st.write("Jumlah duplikasi pada dataframe day: ", day_df.duplicated().sum())

    st.subheader("Missing Values Check")
    if day_df.isnull().values.any():
        st.write("Terdapat missing value dalam DataFrame day:")
        st.write(day_df.isnull().sum())
    else:
        st.write("Tidak ada missing value dalam DataFrame day.")

    st.subheader("Day Dataset Description")
    st.write(day_df.describe())
else:
    st.subheader("Duplicate Check")
    st.write("Jumlah duplikasi pada dataframe hour: ", hour_df.duplicated().sum())

    st.subheader("Missing Values Check")
    if hour_df.isnull().values.any():
        st.write("Terdapat missing value dalam DataFrame hour:")
        st.write(hour_df.isnull().sum())
    else:
        st.write("Tidak ada missing value dalam DataFrame hour.")

    st.subheader("Hour Dataset Description")
    st.write(hour_df.describe())

# Exploratory Data Analysis (EDA)
st.header("Exploratory Data Analysis (EDA)")

if selected_dataset == "Day Dataset":
    st.subheader("Explore Day Dataset")

    st.write(day_df.groupby(by="year").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }))

    st.write(day_df.groupby(by="season").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }).sort_values(by="total_user", ascending=False))

    st.write(day_df.groupby(by="weather_condition").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }).sort_values(by="total_user", ascending=False))

    st.write(day_df.groupby(by="weekday").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }).sort_values(by="total_user", ascending=False))

    st.write(day_df.groupby(by="holiday").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }).sort_values(by="total_user", ascending=False))

    st.write(day_df.groupby(by="workingday").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }).sort_values(by="total_user", ascending=False))

else:
    st.subheader("Explore Hour Dataset")

    st.write(hour_df.groupby(by="year").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }))

    st.write(hour_df.groupby(by="season").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }).sort_values(by="total_user", ascending=False))

    st.write(hour_df.groupby(by="weather_condition").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }).sort_values(by="total_user", ascending=False))

    st.write(hour_df.groupby(by="hour").agg({
        "total_user": "sum",
        "unregistered": "sum",
        "registered": "sum"
    }).sort_values(by="total_user", ascending=False))

# Correlation Heatmap
st.header("Correlation Heatmap")

## Create Correlation Heatmap
if selected_dataset == "Day Dataset":
    df_corr = day_df.corr()
else:
    df_corr = hour_df.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(data=df_corr,
            annot=True,
            annot_kws={'fontsize': 10},
            fmt='.2f',
            cmap='RdYlGn',
            linewidths=.5,
            cbar_kws={"shrink": 0.75})

plt.title(f"{selected_dataset} Correlation Heatmap")
st.pyplot(fig)

# Merge Data
st.header("Merge Data")

all_df = pd.merge(
    left=hour_df,
    right=day_df,
    how="left",
    left_on="datetime",
    right_on="datetime"
)
st.write(all_df.head())

# ---------------------------- Conclusion ------------------------------------------
st.header("Visualization & Explanatory Analysis")

# Select Visualization
selected_visualization = st.selectbox("Select Visualization", ["Pertanyaan 1",
                                                               "Pertanyaan 2",
                                                               "Pertanyaan 3"])

if selected_visualization == "Pertanyaan 1":
    st.subheader("Apakah pengguna sepeda lebih cenderung keluar saat cuaca cerah atau saat cuaca buruk?")

    weather_plot = hour_df[['weather_condition', 'total_user']]
    weather_plot.replace({
        'weather_condition': {
            1: 'Clear',
            2: 'Mist',
            3: 'Light Snow, Light Rain',
            4: 'Heavy Rain, Snow, Fog'
        }
    }, inplace=True)

    weather_plot = weather_plot.groupby('weather_condition')['total_user'].sum().reset_index()
    weather_plot = weather_plot.sort_values('total_user', ascending=False)

    color_list = ['#1565c0', '#bbdefb', '#bbdefb', '#bbdefb']

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
    sns.barplot(data=weather_plot, x='total_user', y='weather_condition', palette=color_list)

    plt.title("Total Bike Users in Different Weather Conditions")
    plt.ylabel(None)
    plt.xlabel("Total Users")

    for p in ax.patches:
        width = p.get_width()
        plt.text(width, p.get_y() + p.get_height() / 2, f"{width:,.0f}", ha='left', va='center')

    st.pyplot(fig)

elif selected_visualization == "Pertanyaan 2":
    st.subheader("Musim apa yang menjadi favorit pengguna untuk bersepeda?")

    color_list = ['#1565c0', '#bbdefb', '#bbdefb', '#bbdefb']

    season_plot = hour_df.groupby('season')['total_user'].sum().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=season_plot, x='season', y='total_user', palette=color_list, ax=ax)

    plt.title("Most Favourite Season to Ride a Bike")
    plt.xlabel('Season')
    plt.ylabel('Total Users')

    st.pyplot(fig)

elif selected_visualization == "Pertanyaan 3":
    st.subheader("Bagaimana performa penjualan perusahaan selama beberapa tahun terakhir?")

    monthly_counts = day_df.groupby('datetime')['total_user'].max().reset_index()

    fig, ax = plt.subplots(figsize=(24, 5))
    sns.scatterplot(x='datetime', y='total_user', data=monthly_counts, color="red", s=10, marker='o')
    sns.lineplot(x='datetime', y='total_user', data=monthly_counts)

    plt.xlabel('Bulan')
    plt.ylabel('Jumlah')
    plt.title('Grafik Jumlah Pelanggan per Bulan pada Tahun 2012')

    st.pyplot(fig)
