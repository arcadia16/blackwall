# FROM python:alpine
#
# RUN mkdir bw_agent
#
# EXPOSE 8091
#
# WORKDIR /bw_agent
#
# COPY . .
#
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
#
# RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
# CMD python -m uvicorn app:app --host 0.0.0.0 --port 8091

# Agent DOES NOT work in container because it tries to invoke docker from docker container
#   AND I don't want to pass it the socket for now