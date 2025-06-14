import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from math import sqrt
import pandas as pd

st.sidebar.title("📘 Dokumentasi")
st.sidebar.markdown("""
Aplikasi ini memiliki 3 model utama:
1. **Linear Programming** (Optimasi Produksi)
2. **EOQ** (Economic Order Quantity)
3. **Model Antrian** (M/M/1)
""")

# Menu utama
menu = st.selectbox("Pilih Model:", ["Optimasi Produksi", "Model EOQ", "Model Antrian"])

# ============================================
# 1. Optimasi Produksi (Linear Programming)
# ============================================
if menu == "Optimasi Produksi":
    st.title("📈 Optimasi Produksi (Linear Programming)")

    st.write("Contoh kasus: Maksimalkan profit dari 2 produk.")

    c = [-40, -30]  # Maksimalkan profit = -minimisasi -profit
    A = [[2, 1],
         [1, 1]]
    b = [100, 80]

    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    st.write("### Hasil Optimasi:")
    st.write(f"Jumlah Produk 1: {res.x[0]:.2f}")
    st.write(f"Jumlah Produk 2: {res.x[1]:.2f}")
    st.write(f"Maksimum Profit: ${-res.fun:.2f}")

    # Visualisasi
    fig, ax = plt.subplots()
    x = np.linspace(0, 60, 400)
    ax.plot(x, (100 - 2*x), label='2x + y ≤ 100')
    ax.plot(x, (80 - x), label='x + y ≤ 80')
    ax.fill_between(x, 0, np.minimum((100 - 2*x), (80 - x)), alpha=0.3)
    ax.set_xlim((0, 60))
    ax.set_ylim((0, 60))
    ax.set_xlabel("Produk 1")
    ax.set_ylabel("Produk 2")
    ax.legend()
    st.pyplot(fig)

# ============================================
# 2. EOQ Model
# ============================================
elif menu == "Model EOQ":
    st.title("📦 Model Persediaan EOQ")

    D = st.number_input("Permintaan Tahunan (D)", min_value=1, value=1000)
    S = st.number_input("Biaya Pemesanan (S)", min_value=1, value=50)
    H = st.number_input("Biaya Penyimpanan per unit/tahun (H)", min_value=1, value=5)

    EOQ = sqrt((2 * D * S) / H)

    st.write(f"### EOQ (Economic Order Quantity): {EOQ:.2f} unit")

    # Grafik EOQ
    Q = np.linspace(1, 500, 100)
    TC = (D / Q) * S + (Q / 2) * H

    fig, ax = plt.subplots()
    ax.plot(Q, TC, label='Total Cost')
    ax.axvline(EOQ, color='red', linestyle='--', label=f'EOQ = {EOQ:.2f}')
    ax.set_xlabel("Order Quantity (Q)")
    ax.set_ylabel("Total Cost")
    ax.legend()
    st.pyplot(fig)

# ============================================
# 3. Model Antrian (M/M/1)
# ============================================
elif menu == "Model Antrian":
    st.title("👥 Model Antrian (M/M/1)")

    λ = st.number_input("Tingkat Kedatangan (λ)", min_value=0.1, value=2.0)
    μ = st.number_input("Tingkat Pelayanan (μ)", min_value=0.1, value=3.0)

    if λ >= μ:
        st.error("Sistem tidak stabil. Pastikan λ < μ.")
    else:
        ρ = λ / μ
        L = ρ / (1 - ρ)
        Lq = ρ**2 / (1 - ρ)
        W = 1 / (μ - λ)
        Wq = ρ / (μ - λ)

        st.write(f"### Utilisasi Sistem (ρ): {ρ:.2f}")
        st.write(f"Rata-rata pelanggan dalam sistem (L): {L:.2f}")
        st.write(f"Rata-rata pelanggan dalam antrian (Lq): {Lq:.2f}")
        st.write(f"Waktu rata-rata dalam sistem (W): {W:.2f} jam")
        st.write(f"Waktu rata-rata dalam antrian (Wq): {Wq:.2f} jam")

        # Grafik Utilisasi
        x_vals = np.linspace(λ, μ - 0.01, 100)
        L_vals = x_vals / (μ - x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, L_vals, label="L vs λ")
        ax.axvline(λ, color='red', linestyle='--', label=f'λ = {λ}')
        ax.set_xlabel("λ (Arrival Rate)")
        ax.set_ylabel("L (Expected in System)")
        ax.legend()
        st.pyplot(fig)
