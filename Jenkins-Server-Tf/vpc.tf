module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name = "jenkins-vpc"
  cidr = "172.20.0.0/16"

  azs = ["us-east-1a"]

  private_subnets = []
  public_subnets  = ["172.20.4.0/24"]

  enable_nat_gateway      = false
  enable_dns_support      = true
  map_public_ip_on_launch = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }

  vpc_tags = {
    Name = "jenkins-vpc"
  }
  igw_tags = {
    Name = "jenkins-igw"
  }
  public_route_table_tags = {
    Name = "jenkins-public-crt"
  }

}
