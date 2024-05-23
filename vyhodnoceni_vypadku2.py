import matplotlib.pyplot as plt
import pandas as pd
####################################
#
#  VSTUPNI UDAJE PRO ZADANI
#
####################################
# Initial constants and variables
MezLo = 60 # Nastavit
MezHi = 100 # Nastavit
PseOKkoefabs = 2 # [MW]
PseOKkoefproc = 2  # [%]
Pinst = 500 # MW - instalovany vykon
Pzasecor = Pinst
####################################
####################################
# Calculate PLMO and VLMO
PLMO = max(PseOKkoefabs, abs(Pzasecor) * 0.01 * PseOKkoefproc)
VLMO = 2 * PLMO

# Specific values of Psecor for the table
# Psecor_values = [200, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 181, 180]

Psecor_values = [ i for i in range(Pinst,int( Pinst - (2*VLMO)), -1)]
print(Psecor_values)
percentage = [i for i in range(0, 105, 10)]
mezhi = [MezHi for i in Psecor_values]
mezlo = [MezLo for i in Psecor_values]
plmo = [PLMO for i in percentage]
vlmo = [VLMO for i in percentage]

# Lists to store abs_diff and PseQproc values
PseQproc_values = []
abs_diff_values = []
Pzasecor_values = []
Psecor_table_values = []

# Calculation loop
for Psecor in Psecor_values:
    abs_diff = abs(Psecor - Pzasecor)
    abs_diff_values.append(abs_diff)
    Pzasecor_values.append(Pzasecor)
    Psecor_table_values.append(Psecor)
    
    if abs_diff <= PLMO:
        PseQproc = 100
    elif abs_diff >= VLMO:
        PseQproc = 0
    else:
        PseQproc = 100 * (1 - ((abs_diff - PLMO) / (VLMO - PLMO)))
    
    PseQproc_values.append(PseQproc)

# Create a DataFrame for the table
data = {
    'Pzasecor': Pzasecor_values,
    'Psecor': Psecor_table_values,
    '|Pzasecor - Psecor|': abs_diff_values,
    'PseQproc': PseQproc_values
}
df = pd.DataFrame(data)

# Print the table
print(df.to_string(index=False))

# Increase the font size for all elements
plt.rcParams.update({'font.size': 14})  # You can adjust the font size here

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(abs_diff_values, PseQproc_values, label='PseQproc vs |Pzasecor - Psecor|', linewidth=4, color='black')
plt.plot(abs_diff_values, mezhi, label=f'MezHi = {MezHi} %', linestyle='-.', linewidth=2, color='gray')
plt.plot(abs_diff_values, mezlo, label=f'MezLo = {MezLo} %', linestyle='-.', linewidth=2, color='gray')
plt.plot(plmo, percentage, label=f'PLMO = {PLMO} MW', linestyle='--', color='gray', linewidth=2)
plt.plot(vlmo, percentage, label=f'VLMO = {VLMO} MW', linestyle='--', color='gray', linewidth=2)

# Add text annotations
#plt.text(abs_diff_values[5], PseQproc_values[5], 'Midpoint', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(abs_diff_values[-1], mezhi[-1], 'MezHi ', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(abs_diff_values[-1], mezlo[-1], 'MezLo ', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(plmo[1], percentage[1], ' PLMO ', fontsize=12, verticalalignment='bottom', horizontalalignment='left')
plt.text(vlmo[1], percentage[1], ' VLMO ', fontsize=12, verticalalignment='bottom', horizontalalignment='left')

plt.xlabel('|Pzasecor - Psecor| [MW]')
plt.ylabel('PseQproc [%]')
plt.title(f'Vyhodnoceni kvality poslouchani zadani na zaklade rozdilu mezi zadanou \n a skutecnou |Pzasecor - Psecor|,\
kde PseOKkoefabs = {PseOKkoefabs} MW a PseOKkoefproc = {PseOKkoefproc} % ')
plt.legend(loc =  'lower right')
plt.grid(True)
plt.show()
