import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from math import sqrt
import pandas as pd

st.set_page_config(page_title="Pemodelan Matematika Industri", layout="wide")

st.sidebar.title("📘 Dokumentasi")
st.sidebar.markdown("""
Aplikasi ini memiliki 3 model:
- **Optimasi Produksi:** Linear Programming
- **Model Persediaan EOQ:** Economic Order Quantity
- **Model Antrian:** Sistem M/M/1

Silakan pilih tab di atas untuk melihat model dan hasilnya.
""")

tab1, tab2, tab3 = st.tabs([
    "📈 Optimasi Produksi (Linear Programming)",
    "📦 Model Persediaan (EOQ)",
    "📊 Model Antrian (M/M/1)"
])

# ====== TAB 1: Linear Programming ======
with tab1:
    st.header("📈 Optimasi Produksi (Linear Programming)")
    st.markdown("Contoh kasus: Maksimalkan profit dari 2 produk.")

    st.sidebar.subheader("Input Linear Programming")
    c1 = st.sidebar.number_input("Profit per Produk 1", value=40)
    c2 = st.sidebar.number_input("Profit per Produk 2", value=30)
    batas1 = st.sidebar.number_input("Batas Kendala 1 (2x + y ≤ ?)", value=100)
    batas2 = st.sidebar.number_input("Batas Kendala 2 (x + y ≤ ?)", value=80)

    c = [-c1, -c2]  # dikali -1 karena linprog meminimalkan
    A = [[2, 1], [1, 1]]
    b = [batas1, batas2]

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')

    if res.success:
        x, y = res.x
        st.subheader("Hasil Optimasi:")
        st.write(f"Jumlah Produk 1: {x:.2f}")
        st.write(f"Jumlah Produk 2: {y:.2f}")
        st.write(f"Maksimum Profit: ${-res.fun:.2f}")

        # Plot grafik
        fig, ax = plt.subplots()
        x_vals = np.linspace(0, 60, 400)
        y1 = (batas1 - 2 * x_vals)
        y2 = (batas2 - x_vals)
        y1 = np.clip(y1, 0, None)
        y2 = np.clip(y2, 0, None)

        ax.plot(x_vals, y1, label="2x + y ≤ " + str(batas1))
        ax.plot(x_vals, y2, label="x + y ≤ " + str(batas2))
        ax.fill_between(x_vals, 0, np.minimum(y1, y2), color='skyblue', alpha=0.4)
        ax.set_xlim(0, max(x_vals))
        ax.set_ylim(0, max(np.max(y1), np.max(y2)))
        ax.set_xlabel("Produk 1")
        ax.set_ylabel("Produk 2")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Optimasi gagal!")

# ====== TAB 2: EOQ ======
with tab2:
    st.header("📦 Model Persediaan EOQ (Economic Order Quantity)")

    st.sidebar.subheader("Input EOQ")
    D = st.sidebar.number_input("Permintaan per tahun (D)", value=1000)
    S = st.sidebar.number_input("Biaya pemesanan per pesanan (S)", value=50)
    H = st.sidebar.number_input("Biaya penyimpanan per unit/tahun (H)", value=2)

    eoq = sqrt((2 * D * S) / H)
    st.subheader("Hasil Perhitungan EOQ:")
    st.write(f"Jumlah pemesanan optimal (EOQ): **{eoq:.2f} unit**")

    fig2, ax2 = plt.subplots()
    q_vals = np.linspace(1, 2 * eoq, 100)
    total_cost = (D / q_vals) * S + (q_vals / 2) * H
    ax2.plot(q_vals, total_cost, label="Total Biaya")
    ax2.axvline(eoq, color='r', linestyle='--', label=f"EOQ ≈ {eoq:.2f}")
    ax2.set_xlabel("Jumlah Pesanan")
    ax2.set_ylabel("Total Biaya")
    ax2.legend()
    st.pyplot(fig2)

# ====== TAB 3: Antrian M/M/1 ======
with tab3:
    st.header("📊 Model Antrian M/M/1")

    st.sidebar.subheader("Input Antrian")
    lambda_ = st.sidebar.number_input("Laju kedatangan (λ)", value=2.0)
    mu = st.sidebar.number_input("Laju pelayanan (μ)", value=3.0)

    if lambda_ >= mu:
        st.error("Model tidak stabil: λ harus lebih kecil dari μ.")
    else:
        rho = lambda_ / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = 1 / (mu - lambda_)
        Wq = rho / (mu - lambda_)

        st.subheader("Hasil Perhitungan:")
        st.write(f"Utilisasi sistem (ρ): {rho:.2f}")
        st.write(f"Rata-rata jumlah dalam sistem (L): {L:.2f}")
        st.write(f"Rata-rata jumlah dalam antrean (Lq): {Lq:.2f}")
        st.write(f"Rata-rata waktu dalam sistem (W): {W:.2f} jam")
        st.write(f"Rata-rata waktu menunggu (Wq): {Wq:.2f} jam")

        df = pd.DataFrame({
            "Metrik": ["ρ", "L", "Lq", "W", "Wq"],
            "Nilai": [rho, L, Lq, W, Wq]
        })
        st.bar_chart(df.set_index("Metrik"))
