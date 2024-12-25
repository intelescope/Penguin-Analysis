import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

df = pd.read_csv("penguins_lter.csv")
df['Date Egg'] = pd.to_datetime(df['Date Egg'], format='%m/%d/%y')

def chart(data):
    
    fig, ax = plt.subplots(figsize=(15, 8))  # 캔버스 크기 조정
    ax.axis('tight')  # 축을 표에 맞춤
    ax.axis('off')    # 축 숨김
    
    # 표 글꼴 크기와 열 너비 조정
    table = ax.table(cellText=data.values, colLabels=data.columns, loc='center', cellLoc='center', colColours=['lightgray']*len(data.columns))

    # 글꼴 크기 조정
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # 열 너비 자동 조정
    table.auto_set_column_width(col=list(range(len(data.columns))))

    # 결과 출력
    plt.show()
    
def species(data):
    # 날짜별 'Species'의 비율 계산
    species_counts_by_date = df.groupby(['Date Egg', 'Species']).size().unstack(fill_value=0)
    species_ratio_by_date = species_counts_by_date.divide(species_counts_by_date.sum(axis=1), axis=0) * 100

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))

    # 날짜별 비율을 그래프에 표시
    species_ratio_by_date.plot(kind='bar', stacked=True, ax=ax)

    # 제목 및 레이블 설정
    ax.set_title('Species Ratio by Date Egg')
    ax.set_xlabel('Date Egg')
    ax.set_ylabel('Percentage (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # 그래프 출력
    plt.show()
    
def gender(data):
    # 날짜별 'gender'의 비율 계산
    gender_counts_by_date = df.groupby(['Date Egg', 'Sex']).size().unstack(fill_value=0)
    gender_ratio_by_date = gender_counts_by_date.divide(gender_counts_by_date.sum(axis=1), axis=0) * 100

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))

    # 날짜별 비율을 그래프에 표시
    gender_ratio_by_date.plot(kind='bar', stacked=True, ax=ax)

    # 제목 및 레이블 설정
    ax.set_title('gender Ratio by Date Egg')
    ax.set_xlabel('Date Egg')
    ax.set_ylabel('Percentage (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # 그래프 출력
    plt.show()
    
def avgmass(data):
    # 연월 정보 추출 (연도-월 형식으로)
    data['Year-Month'] = data['Date Egg'].dt.to_period('M')

    # 연월별 'Body Mass (g)' 평균 계산
    monthly_avg_body_mass = data.groupby('Year-Month')['Body Mass (g)'].mean()

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(12, 6))

    # 막대그래프 생성
    monthly_avg_body_mass.plot(kind='bar', ax=ax)

    # 제목 및 레이블 설정
    ax.set_title('Average Body Mass by Year-Month')
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Average Body Mass (g)')

    # x축 레이블 설정 (연월 표시)
    ax.set_xticklabels(monthly_avg_body_mass.index.astype(str), rotation=45, ha='right')

    plt.tight_layout()
    plt.show()
    
def dNC(data):
    # 연월 정보 추출 (연도-월 형식으로)
    data['Year-Month'] = data['Date Egg'].dt.to_period('M')

    # 연월별 'Delta 15 N (o/oo)' 평균 계산
    dN = data.groupby('Year-Month')['Delta 15 N (o/oo)'].mean()

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(12, 6))

    # 래프 생성
    ax.plot(dN.index.astype(str), dN.values, color='b', marker='o', label='Delta 15 N (o/oo)')
    ax.plot(dN.index.astype(str), dN.values, color='b', marker='o', label='Delta 15 N (o/oo)')

    # 제목 및 레이블 설정
    ax.set_title('Average D15N')
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Delta 15N ratio(permil)')

    # x축 레이블 설정 (연월 표시)
    ax.set_xticklabels(dN.index.astype(str), rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

def relative_destiny_visualizer(data):
    
    def relative_destiny(data, name, axesnum):
        fdf = data[data['Island'] == name]
        Ac = len(fdf[fdf['Species'] == 'Adelie Penguin (Pygoscelis adeliae)'])
        Cc = len(fdf[fdf['Species'] == 'Chinstrap penguin (Pygoscelis antarctica)'])
        Gc = len(fdf[fdf['Species'] == 'Gentoo penguin (Pygoscelis papua)'])
        total = Ac + Cc + Gc
        species_counts = {'Adelie': Ac, 'Chinstrap': Cc, 'Gentoo': Gc}
        species_ratios = {k: 100 * v / total for k, v in species_counts.items() if v > 0}
        Graph = list(species_ratios.values())
        Labels = list(species_ratios.keys())
        colors = {'Adelie': 'blue', 'Chinstrap': 'orange', 'Gentoo': 'green'}
        selected_colors = [colors[label] for label in Labels]
        axes[axesnum].pie(Graph, labels=Labels, autopct='%1.1f%%', startangle=90, colors=selected_colors)
        axes[axesnum].set_title(f'{name} RD ratio')
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    relative_destiny(data, 'Torgersen', 0)
    relative_destiny(data, 'Biscoe', 1)
    relative_destiny(data, 'Dream', 2)
    plt.tight_layout()
    plt.show()
    
    

species(df)
gender(df)
avgmass(df)
dNC(df)
relative_destiny_visualizer(df)