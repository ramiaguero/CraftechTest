# CraftechTest
Entrega de las 3 pruebas tecnicas requeridas para la candidatura

ssh -i craftech.pem ec2-44-203-125-82.compute-1.amazonaws.com
ssh -i craftech.pem ubuntu@ec2-44-203-125-82.compute-1.amazonaws.com

ssh -i craftech.pem ubuntu@ec2-3-82-244-165.compute-1.amazonaws.com
scp -i craftech.pem -r ./* ubuntu@ec2-3-82-244-165.compute-1.amazonaws.com:/opt/myapp/

export const API_SERVER = '/api/';

CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000", "http://ec2-44-203-125-82.compute-1.amazonaws.com"]
