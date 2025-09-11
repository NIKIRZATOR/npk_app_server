FROM dart:3.1.0-sdk

WORKDIR /app

ADD . /app/

RUN dart pub get
RUN dart pub global activate conduit 4.4.0

EXPOSE 6100

ENTRYPOINT [ "dart","pub","run","conduit:conduit","serve","--port","6100" ]