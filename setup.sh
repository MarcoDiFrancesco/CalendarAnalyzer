mkdir -p ~/.streamlit/
echo "[general]\nemail = \"your@example.com\"\n" >~/.streamlit/credentials.toml
echo "[server]\nheadless = true\nenableCORS=false\nport = $PORT\n" >~/.streamlit/config.toml
