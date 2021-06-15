# Load Generator

This load generator is designed to simulate traffic to the ACME Fitness application.

## Apply load to the Istio Ingress Gateway (default)
```
kubectl apply -f loadgen.yaml
```

Edit the `locustfile.py` config in `loadgen.yaml` to modify the load generation profile.