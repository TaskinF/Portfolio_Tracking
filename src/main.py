from get_stock_prices import get_stock_data
import pandas as pd
# Fetch data and create a DataFrame
df = get_stock_data()

# Data cleaning and formatting
df['Hisse Adı'] = df['Hisse Adı'].str.replace(r'\r|\n|\u200b', '', regex=True)
df['Hisse Adı'] = df['Hisse Adı'].astype(str)

# Sort by stock names
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
    'MIATK': {'Maaliyet': 8.65, 'Portföy Lot': 650},
    'YUNSA': {'Maaliyet': 68.85, 'Portföy Lot': 175.48},
    'ASTOR': {'Maaliyet': 120.72, 'Portföy Lot': 127},
    'TTRAK': {'Maaliyet': 837.28, 'Portföy Lot': 14},
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
Toplam_portföy = sum(df_filtered['Güncel Tutar']) + 1364

# Calculate portfolio percentages
def get_stock_group(stock_name):
    if stock_name in ['ASTOR', 'MIATK', 'TUKAS']:
        return 'ATAK'
    elif stock_name in ['GWIND', 'YUNSA']:
        return 'ORTA'
    elif stock_name == 'TTRAK':
        return 'DEFANS'
    else:
        return None  # Returns None if the provided stock name doesn't match any defined group

# Create the 'TÜR' column and fill it with stock groups
df_filtered['Hisse Türü'] = df_filtered['Hisse Adı'].apply(get_stock_group)
df_filtered['% Portföy Oranı'] = ((df_filtered['Güncel Tutar'] / Toplam_portföy) * 100).round(2)
df_filtered['%KAR/ZARAR'] = ((df_filtered['Fiyat'] - df_filtered['Maaliyet']) / df_filtered['Maaliyet'])*100

# Dictionary to store the count of each stock type
stock_type_counts = {
    'ATAK': len(df_filtered[df_filtered['Hisse Türü'] == 'ATAK']),
    'ORTA': len(df_filtered[df_filtered['Hisse Türü'] == 'ORTA']),
    'DEFANS': len(df_filtered[df_filtered['Hisse Türü'] == 'DEFANS'])
}

# Calculate 'DELTA %' based on stock type counts
def calculate_delta(row):
    stock_type = row['Hisse Türü']
    if stock_type == 'ATAK':
        return row['% Portföy Oranı'] - (55 / stock_type_counts['ATAK'])
    elif stock_type == 'ORTA':
        return row['% Portföy Oranı'] - (35 / stock_type_counts['ORTA'])
    elif stock_type == 'DEFANS':
        return row['% Portföy Oranı'] - (10 / stock_type_counts['DEFANS'])
    else:
        return None

# Apply the calculation to create the 'DELTA %' column
df_filtered['DELTA %'] = df_filtered.apply(calculate_delta, axis=1)

# Calculate 'DELTA ₺' column correctly
def calculate_delta_tl(row):
    stock_type = row['Hisse Türü']
    stock_type_count = stock_type_counts.get(stock_type)
    if stock_type_count is None:
        return None

    if stock_type == 'ATAK':
        return row['Güncel Tutar'] - (Toplam_portföy * (0.55 / stock_type_count))
    elif stock_type == 'ORTA':
        return row['Güncel Tutar'] - (Toplam_portföy * (0.35 / stock_type_count))
    elif stock_type == 'DEFANS':
        return row['Güncel Tutar'] - (Toplam_portföy * (0.10 / stock_type_count))
    else:
        return None


# Apply the calculation to create the 'DELTA ₺' column
df_filtered['DELTA ₺'] = df_filtered.apply(calculate_delta_tl, axis=1)

df_filtered['ÇARPAN'] = round(df_filtered['DELTA ₺']/1000,2)

df_filtered = df_filtered.drop(['Hacim(TL)', 'Hacim(Adet)'], axis=1)
# Print the total portfolio value and the filtered DataFrame
print("Toplam portföy : {}".format(Toplam_portföy))
print(df_filtered)