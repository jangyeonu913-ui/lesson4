import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

# 제목 설정
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 열 전처리: 세로막대 기호(|)로 여러 개 적힌 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).str.split("|").str[0]

    return df


# 데이터 로드
df = load_data()

# ---------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수 분포")

# 장르별 영화 수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    values="count",
    names="genre",
    hole=0.4,
    title="장르별 영화 편수 비율",
)

# 마우스 호버 시 편수(value)와 비율(percent) 표시 설정
fig_donut.update_traces(
    hoverinfo="label+value+percent", textinfo="label+percent"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 구분선 및 분석 설명 구역
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("구현하고 싶으신 분석 결과를 여기에 한 문장으로 작성해주세요.")
st.markdown("---")

# ---------------------------------------------------------
# 두 번째 그래프: 장르별/영화별 총 관객 수 (트리맵)
# ---------------------------------------------------------
st.header("2. 장르 및 영화별 총 관객 수 트리맵")

# Plotly 트리맵 생성 (계층 구조: 장르 -> 영화명)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 장르"), "genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객 수 분포",
    hover_data={"total_audi": ":,d"},  # 관객 수를 1,000단위 쉼표 포맷으로 표시
)

# 마우스 호버 시 영화명과 총 관객 수 표시 설정
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_treemap, use_container_width=True)

# 구분선 및 분석 설명 구역
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("구현하고 싶으신 분석 결과를 여기에 한 문장으로 작성해주세요.")
st.markdown("---")
