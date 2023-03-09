#!/bin/bash

ROUTES=("matches/proA")
NUM_REQUESTS=3
OUTPUT_FILE="scripts/response_times.csv"
echo "Route, Temps moyen de réponse (ms)" > $OUTPUT_FILE

for ROUTE in "${ROUTES[@]}"
do
  TOTAL_TIME=0
  for (( i=1; i<=$NUM_REQUESTS; i++ ))
  do
    START_TIME=$(date +%s%N)
    curl -s -o /dev/null -w "%{time_total}\n" http://localhost:8000/$ROUTE
    END_TIME=$(date +%s%N)
    RESPONSE_TIME=$(echo "scale=2; ($END_TIME - $START_TIME) / 1000000" | bc)
    TOTAL_TIME=$(echo "scale=2; $TOTAL_TIME + $RESPONSE_TIME" | bc)
  done
  AVG_TIME=$(echo "scale=2; $TOTAL_TIME / $NUM_REQUESTS" | bc)
  echo "$ROUTE, $AVG_TIME" >> $OUTPUT_FILE
done

echo "Terminé! Les temps de réponse ont été enregistrés dans $OUTPUT_FILE."