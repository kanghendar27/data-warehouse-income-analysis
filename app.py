import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Dashboard Pendapatan KK', layout='wide')
plt.rcParams['figure.dpi'] = 100

# ── Load Data ──
df = pd.read_csv('data/pendapatan_rt013_clean.csv')

pekerjaan_counts = df['pekerjaan'].value_counts()

pend_order = ['Tidak Sekolah', 'SD/Sederajat', 'SMP/Sederajat', 'SMA/Sederajat']
pend_counts = df['pendidikan'].value_counts().reindex(pend_order).dropna()

total_kk = len(df)
mean_pend = df['pendapatan'].mean()
median_pend = df['pendapatan'].median()
total_pend = df['pendapatan'].sum()
max_pend = df['pendapatan'].max()
min_pend = df['pendapatan'].min()
under_umr = (df['pendapatan'] < 4_800_000).sum()
milik_sendiri = (df['status_rumah'] == 'Milik Sendiri').sum()
terima_bantuan = (df['bantuan_sosial'] != 'Tidak Ada').sum()

# ── Sidebar ──
with st.sidebar:
    st.markdown('### Profil Project')
    st.markdown('---')
    st.markdown('**Project:** Analisis Pendapatan Kepala Keluarga')
    st.markdown('**Lokasi:** RT 013 / RW 004, Dusun Ciranggon')
    st.markdown('**Desa:** Ciranggon')
    st.markdown('**Kecamatan:** Majalaya')
    st.markdown('**Kabupaten:** Karawang')
    st.markdown('---')
    st.markdown('**Dataset:** `pendapatan_rt013_clean.csv`')
    st.markdown(f'**Jumlah Data:** {total_kk} Kepala Keluarga')
    st.markdown('---')
    st.markdown('**Mata Kuliah:** Data Warehouse & Business Intelligence')
    st.markdown('**Tahun:** 2026')

# ── Header ──
st.markdown('# Analisis Pendapatan Kepala Keluarga')
st.markdown('### RT 013 / RW 004 Dusun Ciranggon, Desa Ciranggon, Kecamatan Majalaya, Kabupaten Karawang')
st.markdown(
    'Dashboard ini menyajikan hasil analisis pendapatan Kepala Keluarga '
    'menggunakan data dummy yang dirancang menyerupai kondisi riil. '
    'Proyek ini merupakan bagian dari UAS Mata Kuliah Data Warehouse & Business Intelligence.'
)

# ── KPI Cards ──
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric('Jumlah KK', f'{total_kk}')
with col2:
    st.metric('Total Pendapatan', f'Rp{total_pend:,.0f}')
with col3:
    st.metric('Rata-rata', f'Rp{mean_pend:,.0f}')
with col4:
    st.metric('Maksimum', f'Rp{max_pend:,}')
with col5:
    st.metric('Minimum', f'Rp{min_pend:,}')

# ── Visualisasi ──
col_left, col_right = st.columns(2)

with col_left:
    # Distribusi Pekerjaan
    fig, ax = plt.subplots()
    colors_p = ['#2E86AB', '#44994A', '#F18F01']
    bars = ax.bar(pekerjaan_counts.index, pekerjaan_counts.values, color=colors_p, edgecolor='white')
    ax.bar_label(bars, padding=2, fontweight='bold')
    ax.set_title('Distribusi Pekerjaan', fontsize=14, fontweight='bold')
    ax.set_ylabel('Jumlah KK')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)
    plt.close()

with col_right:
    # Distribusi Pendidikan
    fig, ax = plt.subplots()
    colors_d = ['#C73E1D', '#44994A', '#2E86AB', '#A23B72']
    bars = ax.bar(pend_counts.index, pend_counts.values, color=colors_d, edgecolor='white')
    ax.bar_label(bars, padding=2, fontweight='bold')
    ax.set_title('Distribusi Pendidikan', fontsize=14, fontweight='bold')
    ax.set_ylabel('Jumlah KK')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)
    plt.close()

col_left2, col_right2 = st.columns(2)

with col_left2:
    # Histogram Pendapatan
    fig, ax = plt.subplots()
    ax.hist(df['pendapatan'] / 1_000_000, bins=10, edgecolor='white', color='#2E86AB')
    ax.axvline(mean_pend / 1_000_000, color='#C73E1D', linestyle='--', linewidth=1.5,
               label=f"Mean: {mean_pend/1e6:.1f}jt")
    ax.axvline(median_pend / 1_000_000, color='#44994A', linestyle='--', linewidth=1.5,
               label=f"Median: {median_pend/1e6:.1f}jt")
    ax.set_title('Histogram Pendapatan', fontsize=14, fontweight='bold')
    ax.set_xlabel('Pendapatan (juta Rupiah)')
    ax.set_ylabel('Jumlah KK')
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)
    plt.close()

with col_right2:
    # Pendapatan per Pekerjaan (Boxplot)
    fig, ax = plt.subplots()
    pekerjaan_order = df.groupby('pekerjaan')['pendapatan'].median().sort_values().index
    box_data = [df[df['pekerjaan'] == p]['pendapatan'] / 1_000_000 for p in pekerjaan_order]
    bp = ax.boxplot(box_data, tick_labels=pekerjaan_order, patch_artist=True)
    colors_bp = ['#F18F01', '#44994A', '#2E86AB']
    for patch, color in zip(bp['boxes'], colors_bp):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_title('Pendapatan per Pekerjaan', fontsize=14, fontweight='bold')
    ax.set_ylabel('Pendapatan (juta Rupiah)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)
    plt.close()

# ── Insight ──
st.markdown('---')
st.markdown('## Insight Dashboard')

insights = [
    f'Dataset mencakup **{total_kk} Kepala Keluarga** di RT 013 dengan total pendapatan **Rp{total_pend:,.0f}**.',
    f'Rata-rata pendapatan KK adalah **Rp{mean_pend:,.0f}** dengan median **Rp{median_pend:,.0f}**, '
    f'selisih **Rp{mean_pend - median_pend:,.0f}** mengindikasikan distribusi yang menceng ke kanan '
    f'(beberapa KK berpenghasilan tinggi).',
    f'Pekerjaan dominan adalah **{df["pekerjaan"].mode()[0]}** ({pekerjaan_counts.iloc[0]} KK), '
    f'diikuti Petani ({pekerjaan_counts.get("Petani", 0)} KK) dan Pedagang ({pekerjaan_counts.get("Pedagang", 0)} KK).',
    f'Pendidikan terbanyak adalah **{df["pendidikan"].mode()[0]}** ({pend_counts.iloc[0]} KK), '
    f'namun masih terdapat KK yang tidak bersekolah ({pend_counts.get("Tidak Sekolah", 0)} KK).',
    f'Sebanyak **{under_umr} KK ({under_umr/total_kk*100:.0f}%)** memiliki pendapatan di bawah '
    f'UMR Kab. Karawang (Rp4.800.000).',
    f'Sebanyak **{milik_sendiri} KK ({milik_sendiri/total_kk*100:.0f}%)** memiliki rumah sendiri, '
    f'sisanya {total_kk - milik_sendiri} KK masih kontrak atau numpang.',
    f'Penerima bantuan sosial tercatat **{terima_bantuan} KK**, '
    f'terdiri dari PKH ({(df["bantuan_sosial"]=="PKH").sum()} KK) dan '
    f'BPNT ({(df["bantuan_sosial"]=="BPNT").sum()} KK).',
    f'Rata-rata jumlah tanggungan **{df["jumlah_tanggungan"].mean():.1f}** orang per KK, '
    f'dengan rata-rata usia KK **{df["umur"].mean():.0f}** tahun dan '
    f'lama bekerja **{df["lama_bekerja"].mean():.0f}** tahun.',
]

for insight in insights:
    st.markdown(f'- {insight}')
