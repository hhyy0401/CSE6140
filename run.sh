#!/bin/bash

TIME_LIMIT=600

ALG="LS2"

cd "$(dirname "$0")"

# small1 ~ small18
for i in $(seq 1 18); do
    for seed in $(seq 1 10); do
        echo "Running: small${i}, seed=${seed}"
        python exec.py -inst small${i} -alg $ALG -time $TIME_LIMIT -seed $seed
    done
done

# large1 ~ large12
for i in $(seq 1 12); do
    for seed in $(seq 1 10); do
        echo "Running: large${i}, seed=${seed}"
        python exec.py -inst large${i} -alg $ALG -time $TIME_LIMIT -seed $seed
    done
done

# test1 ~ test5
for i in $(seq 1 5); do
    for seed in $(seq 1 10); do
        echo "Running: test${i}, seed=${seed}"
        python exec.py -inst test${i} -alg $ALG -time $TIME_LIMIT -seed $seed
    done
done

#python exec.py -inst large11 -alg LS2 -time 600 -seed 9