# opa cool app


This README provides detailed instructions on how to deploy an Open Policy Agent (OPA) service alongside a web application (opacoolapp) within a Kubernetes cluster managed by Minikube. The web application will communicate with OPA for authorization decisions.

Prerequisites
Minikube: Ensure Minikube is installed on your machine. For installation instructions, visit the official Minikube website.
kubectl: This is the Kubernetes command-line tool that allows you to run commands against Kubernetes clusters. For installation instructions, visit the official Kubernetes documentation.
Docker (Optional): Required if you intend to build Docker images for your application. For Docker installation, visit the Docker website.
Step 1: Start Your Kubernetes Cluster
Open a terminal and start Minikube with your preferred driver. For example, to start Minikube with the Hyper-V driver on Windows, run:

sh
Copy code
minikube start --driver=hyperv
Replace hyperv with your preferred driver (e.g., virtualbox, vmware, etc.).

Once Minikube is started, check the cluster status:

sh
Copy code
minikube status
Step 2: Deploy OPA
Create a ConfigMap for your OPA policies. Assuming your policy file is named policy.rego, create a ConfigMap named opa-policy:

sh
Copy code
kubectl create configmap opa-policy --from-file=policy.rego=path/to/your/policy.rego
Deploy OPA using the deployment YAML file. Assuming the file is named opa-deployment.yaml, apply it:

sh
Copy code
kubectl apply -f opa-deployment.yaml
Deploy the OPA Service. Ensure the service YAML file is correctly set up (usually named opa-service.yaml) and apply it:

sh
Copy code
kubectl apply -f opa-service.yaml
Verify the OPA deployment and service are running:

sh
Copy code
kubectl get pods
kubectl get service opa-service
Step 3: Deploy opacoolapp
Deploy the opacoolapp application using its deployment YAML file. Assuming the file is named opacoolapp-deployment.yaml, apply it:

sh
Copy code
kubectl apply -f opacoolapp-deployment.yaml
Deploy the opacoolapp Service using its service YAML file. Assuming the file is named opacoolapp-service.yaml, apply it:

sh
Copy code
kubectl apply -f opacoolapp-service.yaml
Verify the opacoolapp deployment and service are running:

sh
Copy code
kubectl get pods
kubectl get service opacoolapp-service
Step 4: Testing Communication
To test communication between opacoolapp and the OPA service:

Port Forward (if necessary) to access opacoolapp locally:

sh
Copy code
kubectl port-forward service/opacoolapp-service 8000:8000

6. Exposing Services:
    - Deploy the services to your Minikube cluster.
        - Expose the service 
            kubectl apply -f service.yaml

    - Enable Ingress and create ingress.yaml to expose the Flask app endpoint externally then create secret key to be used as  HTTPS.
        - #Change /etc/hosts : <minikubeId>   my_cool_service
           command : sudo/bin/sh -c 'echo "<minikubeId> my-cool-service" >> etc/hosts"
        - #Generate a Self-Signed Certificate 
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout my-cool-service.key -out my-cool-service.crt -subj "/CN=my-cool-service"
        - #Create a Kubernetes Secret with the self-signed certificate:
            kubectl create secret tls my-cool-service-tls --key my-cool-service.key --cert my-cool-service.crt
        - #update ingress resource to use the secret for TLS:
                #ingress.yaml
                apiVersion: networking.k8s.io/v1
                kind: Ingress
                metadata:
                name: my-cool-service-ingress
                spec:
                tls:
                - hosts:
                    - my-cool-service
                    secretName: my-cool-service-tls
                rules:
                - host: my-cool-service
                    http:
                    paths:
                    - pathType: Prefix
                        path: "/api/users"
                        backend:
                        service:
                            name: my-cool-service
                            port:
                            number: 8000


7. Testing in Kubernetes:
    - Test the endpoints within the Kubernetes cluster to ensure everything is working as expected.