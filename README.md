# opa-flask

1.Setting up the Flask App with Basic Authentication:
    - Create a Flask application in Python in virtual environment (venv).
    - Implement basic authentication for the endpoints using Flask's authentication mechanisms.

2.Integrate OPA for Authorization:
    - Add OPA authorization logic to your Flask application. You'll need to make requests to the OPA service from your Flask app to enforce policies.
    - Define Rego policies to enforce the authorization rules specified in the task.

3.Testing Locally:
    - Test your Flask app and OPA integration locally to ensure that authentication and authorization are working as expected. You can use tools like curl or Postman for testing.
    - Containerize Flask App only (Docker image: /openpolicyagent/opa:edge-rootless):

4.Write Dockerfiles for both the Flask app 
    - Build Docker images for both services and push them to a container registry.

5. Deploying to Minikube:
    - Set up a Minikube Kubernetes cluster.
    - Create Kubernetes YAML files for deploying your Flask app and OPA in the same Pod (sidecar).
    - Deploy the services to your Minikube cluster.
    - Create a ConfigMap for OPA policies.

7. Exposing Services:
    - Expose the Flask app service internally in the cluster.
    - Enable Ingress and create ingress.yaml to expose the Flask app endpoint externally then create secret key to be used as  HTTPS.

9. Testing in Kubernetes:
    - Test the endpoints within the Kubernetes cluster to ensure everything is working as expected.