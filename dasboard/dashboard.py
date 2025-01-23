import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import streamlit as st
import altair as alt
from babel.numbers import format_currency
sns.set(style='dark')

st.set_page_config(
    page_title="Ecommerce Public Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":sunglasses:"
)
alt.theme.enable('dark')

all_data = pd.read_csv('dasboard/all_data.csv')

with st.sidebar:
    st.title("Ecommerce Public Dashboard")
    st.markdown("### Data Overview")
    
    with st.container():
        st.title("Penjualan Berdasarkan Kategori Produk")

        # Pilihan kategori produk
        product_categories = all_data['product_category_name_english'].unique()
        selected_category = st.selectbox("Pilih Kategori Produk", product_categories)

        # Filter data berdasarkan kategori yang dipilih
        filtered_data = all_data[all_data['product_category_name_english'] == selected_category]
        total_sales = filtered_data['total_order_value'].sum()
        formatted_sales = "{:,}".format(int(total_sales)).replace(",", ".")
        # Tampilkan hasil
        st.write(f"Total penjualan untuk kategori **{selected_category}** adalah: {formatted_sales}")
    
    with st.container():
        st.title("Penjualan Berdasarkan Rentang Waktu")

        # Convert order_purchase_timestamp to datetime
        all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])
        all_data['order_year'] = all_data['order_purchase_timestamp'].dt.year

        # Slider untuk memilih rentang tahun
        years = all_data['order_year'].unique()
        start_year, end_year = st.slider(
            "Pilih Rentang Tahun",
            min_value=int(years.min()),
            max_value=int(years.max()),
            value=(int(years.min()), int(years.max()))
        )

        # Filter data berdasarkan rentang tahun
        filtered_data = all_data[
            (all_data['order_year'] >= start_year) & (all_data['order_year'] <= end_year)
        ]
        total_sales = filtered_data['total_order_value'].sum()
        formatted_sales1 = "{:,}".format(int(total_sales)).replace(",", ".")
        # Tampilkan hasil
        st.write(f"Total penjualan dari tahun **{start_year}** hingga **{end_year}** adalah: {formatted_sales1}")
    
    st.caption("By Adam Havenia Pratama")

def prepare_heatmap_data(df):
    # Extract hour from order_purchase_timestamp
    df['hour'] = df['order_purchase_timestamp'].dt.hour

    # Create a pivot table
    heatmap_data = df.pivot_table(values='total_order_value', 
                                  index='hour', 
                                  columns='order_dayofweek', 
                                  aggfunc='sum')
    return heatmap_data

def get_top_product_categories(df, top_n=10):
    # Group by product category and sum the order item counts
    top_product_category = (
        df.groupby("product_category_name_english")["total_order_value"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    return top_product_category

def get_top_cities_by_sales(df, top_n=10):
    # Group by customer city and sum total order value
    top_city_by_sales = (
        df.groupby("customer_city")["total_order_value"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    return top_city_by_sales

def get_monthly_sales(df):
    # Group by 'order_month' and sum 'total_order_value'
    monthly_sales = (
        df.groupby('order_month')['total_order_value']
        .sum()
        .reset_index()
        .sort_values(by='order_month')
    )
    return monthly_sales

def get_daily_sales(df):
    # Group by 'order_dayofweek' and sum 'total_order_value'
    daily_sales = (
        df.groupby('order_dayofweek')['total_order_value']
        .sum()
        .reset_index()
        .sort_values(by='order_dayofweek')
    )
    return daily_sales

def get_yearly_sales(df):
    # Group by 'order_year' and sum 'total_order_value'
    yearly_sales = (
        df.groupby('order_year')['total_order_value']
        .sum()
        .reset_index()
        .sort_values(by='order_year')
    )
    return yearly_sales

def get_payment_sales(df):
    # Group by 'payment_type' and sum 'total_order_value'
    payment_sales = (
        df.groupby('payment_type')['total_order_value']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return payment_sales

def get_payment_avg(df):
    # Group by 'payment_type' and calculate the mean of 'total_order_value'
    payment_avg = (
        df.groupby('payment_type')['total_order_value']
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    payment_avg.rename(columns={'total_order_value': 'average_order_value'}, inplace=True)
    return payment_avg


def get_order_count_by_review(df):
    # Calculate the count of orders for each review score
    order_count_by_review = (
        df['review_score']
        .value_counts()
        .sort_index()
        .reset_index()
        .rename(columns={'index': 'p', 'review_score': 'order_count'})
    )
    return order_count_by_review

def get_customer_type_counts(df):
    # Count the occurrences of each customer type
    customer_type_counts = (
        df['is_new_customer']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'customer_type', 'is_new_customer': 'customer_count'})
    )
    # Map boolean values to descriptive labels (optional)
    customer_type_counts['customer_type'] = customer_type_counts['customer_type'].map({
        True: 'New Customer',
        False: 'Returning Customer'
    })
    return customer_type_counts

all_data = pd.read_csv('dasboard/all_data.csv')

with st.container():
    st.title("Produk yang paling banyak dibeli")

    # Gunakan helper function untuk mendapatkan top product categories
    top_product_category = get_top_product_categories(all_data, top_n=10)
    custom_colors = ['#004D4D','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6']

  
    order_count_by_review = get_order_count_by_review(all_data)
    plt.figure(figsize=(12, 6))
    sns.barplot(
    x=top_product_category["total_order_value"], 
    y=top_product_category["product_category_name_english"],
    palette=custom_colors
    )

    plt.xlabel("Total Pesanan")
    plt.ylabel("")
    plt.tight_layout()

    # Tampilkan plot di Streamlit
    st.pyplot(plt)
    st.write("Dari informasi tersebut dapat disimpulkan bahwa produk yang paling banyak dibeli adalah produk kategori 'health_beauty'.")

with st.container():
    st.title("Kota dengan penjualan terbanyak")
    custom_colors = ['#004D4D','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6']

    # Gunakan helper function untuk mendapatkan top cities by sales
    top_city_by_sales = get_top_cities_by_sales(all_data, top_n=10)
    plt.figure(figsize=(12, 6))
    sns.barplot(
    x=top_city_by_sales["total_order_value"], 
    y=top_city_by_sales["customer_city"],
    palette=custom_colors
    )

    plt.xlabel("Total Penjualan (Rupiah)")
    plt.ylabel("")
    plt.tight_layout()

    # Tampilkan plot di Streamlit
    st.pyplot(plt)
    st.write("Dari informasi tersebut dapat disimpulkan bahwa kota dengan penjualan terbanyak adalah kota 'sao paulo'.")

with st.container():
    st.subheader("Jika kepo penjualan di kota lain, silakan pilih kota yang ingin dilihat penjualannya.")

    # Multiselect untuk memilih kota
    cities = all_data['customer_city'].unique()
    selected_cities = st.multiselect("Pilih Kota", cities)

    if selected_cities:
        # Filter data berdasarkan kota yang dipilih
        filtered_data = all_data[all_data['customer_city'].isin(selected_cities)]
        city_sales = (
            filtered_data.groupby('customer_city')['total_order_value']
            .sum()
            .reset_index()
            .sort_values(by='total_order_value', ascending=False)
        )

        # Tampilkan data
        st.write("Total penjualan untuk kota yang dipilih:")
        st.dataframe(city_sales)
        color4 = ['#004D4D','#ADD8E6','#FF6F91']
        # Visualisasi data
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x='total_order_value', 
            y='customer_city', 
            data=city_sales, 
            palette=color4
        )
        plt.title("Total Penjualan Berdasarkan Kota")
        plt.xlabel("Total Penjualan (Rupiah)")
        plt.ylabel("")
        plt.tight_layout()
        st.pyplot(plt)


with st.container():
    st.title("Waktu yang memiliki penjualan terbanyak")
    col1, col2, col3 = st.columns([1, 1, 1])
    color1 = ['#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#004D4D','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6']
    color2= ['#004D4D','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6','#ADD8E6']
    color3= ['#ADD8E6','#ADD8E6','#004D4D']
    monthly_sales = get_monthly_sales(all_data)
    daily_sales = get_daily_sales(all_data)

    with col2:
        st.write("Penjualan Bulanan: ")
        plt.figure(figsize=(12, 6))
        sns.barplot(
        x=monthly_sales['order_month'], 
        y=monthly_sales['total_order_value'],
        palette=color1
        )

        plt.title("Total Penjualan berdasarkan Bulan")
        plt.xlabel("Bulan (1=Januari, 12=Desember)")
        plt.ylabel("Total nilai penjualan")
        plt.xticks(rotation=0)  # Rotasi untuk nama bulan
        plt.tight_layout()
        st.pyplot(plt)

    with col1:
        st.write("Penjualan Harian:")
        plt.figure(figsize=(12, 6))
        sns.barplot(
        x=daily_sales['order_dayofweek'], 
        y=daily_sales['total_order_value'],
        palette=color2
        )

        plt.title("Total Penjualan berdasarkan Hari dalam Seminggu")
        plt.xlabel("Hari dalam Seminggu (0=Senin, 6=Minggu)")
        plt.ylabel("Total nilai penjualan")
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(plt)

    with col3:
        st.write("Penjualan Tahunan:")
        yearly_sales = get_yearly_sales(all_data)
        plt.figure(figsize=(12, 6))
        sns.barplot(
        x=yearly_sales['order_year'], 
        y=yearly_sales['total_order_value'],
        palette=color3
        )

        plt.title("Total Penjualan berdasarkan Tahun")
        plt.xlabel("Tahun")
        plt.ylabel("Total nilai penjualan")
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(plt)

    st.write("Dari informasi tersebut dapat disimpulkan bahwa penjualan terbanyak terjadi pada bulan 'Mei', hari 'Senin', dan tahun '2018'.")
    #   Pastikan kolom order_purchase_timestamp sudah dalam format datetime
    all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])

    # Gunakan helper function untuk mempersiapkan data heatmap
    heatmap_data = prepare_heatmap_data(all_data)

    # Menggunakan palet warna custom
    custom_palette = ['#ADD8E6', '#004D4D', '#FF6F91', '#FFF5E1', '#2E2C6B']
    sns.heatmap(heatmap_data, cmap=sns.color_palette(custom_palette, as_cmap=True), 
                annot=True, fmt=".0f", linewidths=0.5)
    plt.title("Penjualan Berdasarkan Hari dan Jam", fontsize=16, fontweight='bold')
    plt.xlabel("Hari dalam Seminggu (0=Senin, 6=Minggu)", fontsize=14)
    plt.ylabel("Jam", fontsize=14)
    # Tampilkan heatmap di Streamlit
    plt.tight_layout()
    st.pyplot(plt)
    st.write("Dari informasi tersebut dapat disimpulkan bahwa penjualan terbanyak terjadi pada hari 'Senin' dan dengan rata rata jam sibuknya adalah pukul 10.00 hingga pukul 22.00.")


with st.container():
    st.title("Pembayaran yang paling banyak digunakan")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("Total Penjualan berdasarkan Jenis Pembayaran:")
        color1 = ['#FF6F91','#ADD8E6','#ADD8E6','#ADD8E6']
        color2 = ['#FF6F91','#ADD8E6','#ADD8E6','#ADD8E6']
        payment_sales = get_payment_sales(all_data)
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x=payment_sales['total_order_value'], 
            y=payment_sales['payment_type'],
            palette=color1
        )

        plt.xlabel("Total Penjualan")
        plt.ylabel("Tipe Pembayaran")
        plt.tight_layout()

        # Tampilkan plot di Streamlit
        st.pyplot(plt)
    
    with col2:
        st.write("Penjualan Rata-rata berdasarkan Jenis Pembayaran:")
        payment_avg = get_payment_avg(all_data)
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x=payment_avg['average_order_value'], 
            y=payment_avg['payment_type'],
            palette=color2
        )

        plt.xlabel("Nilai Rata-rata Penjualan")
        plt.ylabel("")
        plt.tight_layout()

        # Tampilkan plot di Streamlit
        st.pyplot(plt)
    
    st.write("Dari informasi tersebut dapat disimpulkan bahwa metode pembayaran yang paling banyak digunakan adalah 'credit_card' dan memiliki rata rata pembelian terbesar.")

def visualize_order_count_review_score(all_df):
    # Hitung jumlah order berdasarkan review_score
    order_count_by_review = all_df['review_score'].value_counts().sort_index()

    # Warna untuk visualisasi
    color1 = ['#ADD8E6', '#ADD8E6', '#ADD8E6', '#ADD8E6', '#2E2C6B']

    # Membuat visualisasi di Streamlit
    with st.container():
        st.title("Hasil Review Pelanggan (Review Score)")
        
        # Membuat plot
        plt.figure(figsize=(15, 6))

        # Subplot: Number of orders by review score
        sns.barplot(
            x=order_count_by_review.index, 
            y=order_count_by_review.values, 
            palette=color1
        )
        plt.xlabel('Review Score')
        plt.ylabel('')

        plt.tight_layout()

        # Tampilkan plot di Streamlit
        st.pyplot(plt)
        st.write("Dari informasi tersebut dapat disimpulkan bahwa review score yang paling banyak diberikan adalah '5', hal ini menunjukan bahwa customer banyak menyukai produk yang ditawarkan.")

# Call the function to visualize order count by review score
visualize_order_count_review_score(all_data)

def visualize_customer_distribution(All_df):
    # Hitung jumlah pelanggan baru vs pelanggan lama
    customer_type_counts = All_df['is_new_customer'].value_counts()

    # Membuat visualisasi di Streamlit
    with st.container():
        st.title("Distribusi Pelanggan Baru vs Pelanggan Lama")
        
        # Membuat pie chart
        plt.figure(figsize=(10, 6))
        plt.pie(
            customer_type_counts, 
            labels=['Pelanggan Lama', 'Pelanggan Baru'], 
            autopct='%1.1f%%',
            colors=['#ADD8E6', '#FFF5E1']
        )
        plt.title('Perbandingan Pelanggan Baru vs Pelanggan Lama')
        plt.axis('equal')  # Pastikan pie chart berbentuk lingkaran

        # Tampilkan plot di Streamlit
        st.pyplot(plt)

        # Menampilkan jumlah aktual
        st.subheader("Jumlah Pelanggan:")
        st.write(f"Pelanggan Lama: {customer_type_counts[True]:,}")
        st.write(f"Pelanggan Baru: {customer_type_counts[False]:,}")
        st.write("Dari informasi tersebut dapat disimpulkan bahwa jumlah pelanggan baru lebih banyak dibandingkan dengan pelanggan lama.")
visualize_customer_distribution(all_data) 

