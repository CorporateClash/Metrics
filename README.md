# Clash Metrics

Reports component status and metrics to cachet status page via Lambda.



#### Env Vars and Setup

see [serverless.yml](serverless.yml)

set up the `ssm:` variables by running

    aws ssm put-parameter --name cachet_token --type String --value TokenHere
    aws ssm put-parameter --name login_password --type String --value PassHere

#### License

MIT licensed. For more information see [LICENSE.md](LICENSE.md).