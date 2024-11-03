import pandas as pd
from scipy import stats

# Load your data
data = pd.read_csv('postcodes.csv')

# Filter Sydney and other suburbs
sydney_data = data[data['nsw_loca_2'] == 'SYDNEY']['countRate']
other_data = data[data['nsw_loca_2'] != 'SYDNEY']['countRate']

# Drop NaN values
sydney_data = sydney_data.dropna()
other_data = other_data.dropna()

# Perform a one-sided independent t-test
t_stat, p_value = stats.ttest_ind(sydney_data, other_data, alternative='greater', equal_var=False)

# Display the results
print(f"T-statistic: {t_stat:.3f}")
print(f"P-value: {p_value:.3f}")

if p_value < 0.05:
    print("Reject the null hypothesis. The count rate in Sydney is significantly higher than in other suburbs.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference in count rate between Sydney and other suburbs.")