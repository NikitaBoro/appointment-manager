# appointment-manager

Clone:\
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-V/appointment-manager.git \
cd appointment-manager \

Build and run Docker:\
docker build -t appointment-manager . -f Dockerfile \
docker run -p8888:8000 appointment-manager  \
Access at: http://localhost:8888/docs \

Run tests:\
pytest ./backend/unit_test.py \
pytest integration_test.py  \
