#import "@preview/basic-resume:0.2.9": *

#let name = "John Doe"
#let location = "San Francisco, CA"
#let email = "john.doe@email.com"
#let linkedin = "linkedin.com/in/johndoe"
#let github = "github.com/johndoe"

#show: resume.with(
  author: name,
  location: location,
  email: email,
  linkedin: linkedin,
  github: github,
  accent-color: "#26428b",
  font: "New Computer Modern",
  paper: "us-letter",
  author-position: left,
  personal-info-position: left,
)

== Professional Experience

#work(
  title: "Software Engineer, Model Infrastructure",
  location: "San Francisco, CA",
  company: "Anthropic",
  dates: dates-helper(start-date: "July 2024", end-date: "Present"),
)
- Designed and maintained high-throughput inference infrastructure serving Claude API traffic at scale, achieving 99.99% uptime across multi-region deployments.
- Built distributed batching and scheduling systems in Python and C++ to optimize GPU utilization across thousands of accelerators, reducing inference cost by 30%.
- Developed internal tooling for model evaluation pipelines, enabling rapid iteration across safety and capability benchmarks for pre-release model versions.
- Collaborated with research teams to productionize new model architectures, owning the full path from prototype to serving infrastructure.

#work(
  title: "Software Engineer, Market Data & Connectivity",
  location: "New York, NY",
  company: "Hudson River Trading",
  dates: dates-helper(start-date: "July 2023", end-date: "June 2024"),
)
- Developed ultra-low-latency market data processing pipelines in C++ handling 10M+ messages/second with sub-microsecond processing overhead.
- Optimized critical path network I/O using kernel bypass (DPDK) and lock-free data structures, reducing median tick-to-order latency by 40%.
- Built and maintained exchange connectivity adapters for equities and futures venues across US and European markets.
- Contributed to internal simulation framework used to replay historical market data for strategy backtesting and system regression testing.

#work(
  title: "Software Engineering Intern",
  location: "Seattle, WA",
  company: "Amazon Web Services",
  dates: dates-helper(start-date: "June 2022", end-date: "August 2022"),
)
- Built a distributed tracing feature for AWS Lambda, surfacing cold start latency breakdowns in CloudWatch, shipped to production and used by 10k+ customers.
- Wrote automated integration tests across 3 AWS regions, catching 2 critical regressions before release.

== Education

#edu(
  institution: "Massachusetts Institute of Technology (MIT)",
  location: "Cambridge, MA",
  dates: dates-helper(start-date: "September 2019", end-date: "June 2023"),
  degree: "B.S. Computer Science & Engineering | GPA: 4.8/5.0",
)

== Skills
*Programming*: C++ (expert), Python (expert), Rust (proficient), Go, Bash \
*Systems*: Distributed systems, low-latency networking, DPDK, lock-free concurrency, CUDA \
*ML Infrastructure*: Model serving, inference optimization, GPU scheduling, PyTorch \
*Tools*: Git, Linux, Docker, Kubernetes, AWS (EC2, Lambda, CloudWatch) \
*Languages*: English (Native), Spanish (Conversational)
