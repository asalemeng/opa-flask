# opa-flask
![alt text](image.png)

1. Setting up the Flask App with Basic Authentication:
    - Create a Flask application in Python in virtual environment (venv).
         - #install venv virtual: python -m venv venv 
         - #activate venv : venv\Scripts\activate.ps1
         - #install required packages : pip install -r requirements.txt
    - Implement basic authentication for the endpoints using Flask's authentication mechanisms.

2. Integrate OPA for Authorization:
    - Add OPA authorization logic to your Flask application. You'll need to make requests to the OPA service from your Flask app to enforce policies.
    - Define Rego policies to enforce the authorization rules specified in the task.
        use https://play.openpolicyagent.org/ for testing 

3. Testing Locally:
    - Test your Flask app and OPA integration locally to ensure that authentication and authorization are working as expected. You can use tools like curl or Postman for testing.
    - Containerize Flask App only (Docker image: /openpolicyagent/opa:edge-rootless):

4. Write Dockerfiles for both the Flask app 
    - Build Docker images for both services and push them to a container registry.

5. Deploying to Minikube:
    - Set up a Minikube Kubernetes cluster.
        - I created a Deployment definition yaml that I used to deploy in my Kubernetes cluster. The deployment specifies a Pod containing two containers:
            - my-cool-service flask app
            - OPA server 
               - we can create ConfigMaps with our Policy opaweb-policy.rego file, and put it in the OPA Container.
                    $ kubectl create configmap opademo-policy --from-file=opaweb-policy.rego
    - Create Kubernetes YAML files for deploying your Flask app and OPA in the same Pod (sidecar).
        - Deploy deployment.yaml :
            kubectl apply -f deployment.yaml 

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