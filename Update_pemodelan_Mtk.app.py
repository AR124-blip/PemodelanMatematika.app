import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from math import sqrt

# Sidebar dokumentasi
st.sidebar.title("📘 Dokumentasi")
st.sidebar.markdown("""
Aplikasi ini memiliki 3 model utama:
1. **Optimasi Produksi** (Linear Programming)
2. **EOQ** (Economic Order Quantity)
3. **Model Antrian** (M/M/1)
""")

# Navigasi menu
menu = st.selectbox("📊 Pilih Model:", ["Optimasi Produksi", "Model EOQ", "Model Antrian"])

# ================================
# 1. Optimasi Produksi
# ================================
if menu == "Optimasi Produksi":
    st.title("📈 Optimasi Produksi (Linear Programming)")
    st.write("Masukkan data keuntungan dan batas sumber daya:")

    st.sidebar.header("Input Parameter")

    # Input dari user
    profit_x = st.sidebar.number_input("Profit per Produk 1", value=40)
    profit_y = st.sidebar.number_input("Profit per Produk 2", value=30)
    batas1 = st.sidebar.number_input("Batas Kendala 1 (2x + y ≤ ?)", value=100)
    batas2 = st.sidebar.number_input("Batas Kendala 2 (x + y ≤ ?)", value=80)

    if st.button("Hitung Optimasi"):
        # Fungsi objektif (negatif karena linprog meminimalkan)
        c = [-profit_x, -profit_y]
        A = [[2, 1], [1, 1]]
        b = [batas1, batas2]
        bounds = [(0, None), (0, None)]

        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if result.success:
            x_opt, y_opt = result.x
            st.subheader("🔍 Hasil Optimasi:")
            st.write(f"Jumlah Produk 1 (x): {x_opt:.2f}")
            st.write(f"Jumlah Produk 2 (y): {y_opt:.2f}")
            st.write(f"Total Profit Maksimum: ${-result.fun:.2f}")

            # Visualisasi
            x = np.linspace(0, max(batas1, batas2), 400)
            y1 = (batas1 - 2 * x)
            y2 = (batas2 - x)

            fig, ax = plt.subplots()
            ax.plot(x, y1, label=f"2x + y ≤ {batas1}")
            ax.plot(x, y2, label=f"x + y ≤ {batas2}")
            ax.fill_between(x, 0, np.minimum(y1, y2), where=(y1 >= 0) & (y2 >= 0), color='skyblue', alpha=0.4)
            ax.plot(x_opt, y_opt, 'ro', label="Titik Optimal")
            ax.set_xlim((0, max(batas1, batas2)))
            ax.set_ylim((0, max(batas1, batas2)))
            ax.set_xlabel("Produk 1 (x)")
            ax.set_ylabel("Produk 2 (y)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.error("❌ Gagal menemukan solusi optimal. Coba periksa input Anda.")

# ================================
# 2. EOQ Model
# ================================
elif menu == "Model EOQ":
    st.title("📦 Model Persediaan EOQ")

    D = st.number_input("Permintaan Tahunan (D)", min_value=1, value=1000)
    S = st.number_input("Biaya Pemesanan per Order (S)", min_value=1, value=50)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", min_value=1, value=5)

    EOQ = sqrt((2 * D * S) / H)
    st.subheader(f"📦 EOQ: {EOQ:.2f} unit per pesanan")

    # Grafik Total Cost
    Q = np.linspace(1, 2 * EOQ, 100)
    TC = (D / Q) * S + (Q / 2) * H

    fig, ax = plt.subplots()
    ax.plot(Q, TC, label='Total Cost')
    ax.axvline(EOQ, color='red', linestyle='--', label=f'EOQ = {EOQ:.2f}')
    ax.set_xlabel("Order Quantity (Q)")
    ax.set_ylabel("Total Cost")
    ax.legend()
    st.pyplot(fig)

# ================================
# 3. Model Antrian
# ================================
elif menu == "Model Antrian":
    st.title("👥 Model Antrian (M/M/1)")

    λ = st.number_input("Tingkat Kedatangan (λ)", min_value=0.1, value=2.0)
    μ = st.number_input("Tingkat Pelayanan (μ)", min_value=0.1, value=3.0)

    if λ >= μ:
        st.error("❌ Sistem tidak stabil. Pastikan λ < μ.")
    else:
        ρ = λ / μ
        L = ρ / (1 - ρ)
        Lq = ρ**2 / (1 - ρ)
        W = 1 / (μ - λ)
        Wq = ρ / (μ - λ)

        st.subheader("📊 Hasil Perhitungan Antrian:")
        st.write(f"Utilisasi Sistem (ρ): {ρ:.2f}")
        st.write(f"Rata-rata pelanggan dalam sistem (L): {L:.2f}")
        st.write(f"Rata-rata pelanggan dalam antrian (Lq): {Lq:.2f}")
        st.write(f"Waktu rata-rata dalam sistem (W): {W:.2f} satuan waktu")
        st.write(f"Waktu rata-rata dalam antrian (Wq): {Wq:.2f} satuan waktu")

        # Grafik L vs λ
        x_vals = np.linspace(0.01, μ - 0.01, 100)
        L_vals = x_vals / (μ - x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, L_vals, label="L vs λ")
        ax.axvline(λ, color='red', linestyle='--', label=f'λ = {λ}')
        ax.set_xlabel("Tingkat Kedatangan (λ)")
        ax.set_ylabel("Jumlah Pelanggan dalam Sistem (L)")
        ax.legend()
        st.pyplot(fig)
