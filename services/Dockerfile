FROM python3:12-slim
WORKDIR /app
COPY . /app/
EXPOSE 8765 8766 8770 8775 8777 8780 8790
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8765/api/health')" || exit 1
CMD ["python3", "server.py"]
