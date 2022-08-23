import pandas as pd


fake = pd.DataFrame(
    [[4,4,4,4]],
    columns=('서비스', '음식', '편의성', '가격')
    )
fake.to_csv('fake.csv', index=False)