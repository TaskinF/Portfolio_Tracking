from get_stock_prices import get_stock_data

# Fetch data and create a DataFrame
df = get_stock_data()

# Data cleaning and formatting
df['Hisse Adı'] = df['Hisse Adı'].str.replace(r'\r|\n|\u200b', '', regex=True)
df['Hisse Adı'] = df['Hisse Adı'].astype(str)

# Sort by Stock Name
df = df.sort_values(by='Hisse Adı', ascending=True)

# Remove single quotes
df['Hisse Adı'] = [x.split()[0].strip("'") for x in df['Hisse Adı']]

# Define target stocks
hedef_hisseler = ['GWIND', 'TUKAS', 'MIATK', 'YUNSA', 'ASTOR', 'TTRAK', 'EUPWR', 'HATSN']
hisse_türü = {
    'ATAK': {'Tür %': 55},
    'ORTA': {'Tür %': 35},
    'DEFANS': {'Tür %': 10},
}
# Dictionary of maaliyet and portföy lot for each stock
hisse_bilgileri = {
    'GWIND': {'Maaliyet': 20.13, 'Portföy Lot': 484.13},
    'TUKAS': {'Maaliyet': 6.94, 'Portföy Lot': 1697},
    'MIATK': {'Maaliyet': 112.49, 'Portföy Lot': 50},
    'YUNSA': {'Maaliyet': 68.85, 'Portföy Lot': 175.48},
    'ASTOR': {'Maaliyet': 120.72, 'Portföy Lot': 127},
    'TTRAK': {'Maaliyet': 846.03, 'Portföy Lot': 13},
    'EUPWR': {'Maaliyet': 40.60, 'Portföy Lot': 25},
    'HATSN': {'Maaliyet': 22.60, 'Portföy Lot': 8}
}
# Filter for target stocks
df_filtered = df[df['Hisse Adı'].isin(hedef_hisseler)].copy()

# Portfolio data
maaliyet_list = [hisse_bilgileri[hisse]['Maaliyet'] for hisse in df_filtered['Hisse Adı']]
portfoy_lot_list = [hisse_bilgileri[hisse]['Portföy Lot'] for hisse in df_filtered['Hisse Adı']]
df_filtered['Maaliyet'] = maaliyet_list
df_filtered['Portföy Lot'] = portfoy_lot_list
df_filtered['Fiyat'] = df_filtered['Fiyat'].str.replace(',', '.').astype(float)
df_filtered['Güncel Tutar'] = df_filtered['Fiyat'] * df_filtered['Portföy Lot']
df_filtered['₺ KAR/ZARAR '] = df_filtered['Güncel Tutar'] - (df_filtered['Maaliyet'] * df_filtered['Portföy Lot'])

# Calculate total portfolio (including cash amount)
Toplam_portföy = sum(df_filtered['Güncel Tutar']) + 27.0

# Calculate portfolio percentages
df_filtered['% Portföy Oranı'] = ((df_filtered['Güncel Tutar'] / Toplam_portföy) * 100).round(2)
df_filtered['%KAR/ZARAR'] = (df_filtered['Fiyat'] - df_filtered['Maaliyet']) / df_filtered['Maaliyet']
df_filtered['DELTA %'] = (df_filtered['% Portföy Oranı'])

# Print the total portfolio value and the filtered DataFrame
print(df_filtered)
print(Toplam_portföy)
