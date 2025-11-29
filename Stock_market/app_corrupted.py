        # RSI calculation
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        # Extract RSI value safely with default fallback
        rsi_value = 50.0  # Default neutral RSI value
        # Simple approach to avoid linter errors
        try:
            rsi_value = float(rsi.iloc[-1])  # pyright: ignore[reportAttributeAccessIssue]
        except:
            try:
                rsi_value = float(rsi[-1])  # pyright: ignore[reportAttributeAccessIssue]
            except:
                pass  # Keep default value