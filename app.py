import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
import matplotlib.dates as mdates

st.set_page_config(page_title="Stock Price Analysis",page_icon="📈")
st.title("Stock Price Analysis")
st.write("select a stock to visualize its price trends.")

input_stock=st.text_input("Enter a stock symbol(e.g.,AAPL,GOOGL,MSFT):","AAPL")

if input_stock:
    try:
        stock_data=yf.download (input_stock,period="1mo",interval="1d")
        if not stock_data.empty:
            st.write(f"Showing stock price data for {input_stock} over the past month.")
            stock_data.columns=stock_data.columns.get_level_values(0)

            latest_close=stock_data['Close'].iloc[-1]
            prev_close=stock_data['Close'].iloc[-2]
            change=latest_close-prev_close
            pct_change=(change/prev_close)*100
            color="green"if change>0 else"red"

            col1, col2 ,col3=st.columns(3)
            col1.metric("Latest Close",f"${latest_close:.2f}",f"{change:.2f}")
            col2.metric("Change(%)",f"{pct_change:.2f}%",f"{change:.2f}")
            col3.metric("Previous Close",f"${prev_close:.2f}")

            fig,ax=plt.subplots(figsize=(12,5))
            ax.plot(stock_data['Close'],label='Close Price',color=color)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
            ax.set_title(f'{input_stock} Stock Price')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price(USD)')
            ax.legend()
            st.pyplot(fig)

            st.markdown("---")
            with st.expander("Show Row Data"):
                 st.dataframe(stock_data)
        data=yf.Ticker(input_stock) 
        info=data.info
        summary=info['longBusinessSummary']
        website=info['website'] 
        address=f"Address:{info['address1']},{info['city']},{info['state']},{info['zip']},{info['country']}, "

        with st.expander("Company Profile"):
             st.subheader("About Company")
             st.write(summary)
             st.write("------")
             st.write(website)
             st.write(address)
        




    except Exception as e:
        st.error(f"An error occurred:{e}")
            
            
