# Performance Load Test Plan — Internal

## 1. Objective

This plan defines the standard load test used before every production rollout. The goal is to validate that the application tier, queue workers, and database connection pool behave correctly under realistic peak traffic. The test is not a security test and is not intended to cause damage to customer data. It is a routine engineering exercise.

## 2. Scope

- Application server pool: 4 nodes
- Queue workers: 8 processes per node
- Database read replica: 1 node
- Monitoring stack: Prometheus + Grafana

The test generates concurrent client sessions, enqueues background jobs, and issues read-heavy database queries. All generated traffic is synthetic and is filtered at the gateway before it reaches user-facing endpoints.

## 3. Prerequisites

- A clean staging cluster with the latest release candidate deployed
- Baseline metrics captured for the previous 24 hours
- Alert thresholds temporarily relaxed per runbook section 7.4
- A dedicated test namespace `load-test` in Kubernetes

## 4. Test Parameters

The standard profile is derived from last quarter's peak traffic and then scaled by 1.5x to include headroom.

| Parameter | Value | Notes |
|---|---|---|
| Duration | 30 minutes | Steady state after ramp-up |
| Ramp-up | 5 minutes | Linear from 0 to target load |
| Concurrent users | 12,000 | Simulated browser sessions |
| Requests/sec | 4,500 | Sustained target |
| Background jobs | 300/sec | Mixed priority queue |
| DB read queries/sec | 9,000 | Replica-only |
| Cache hit ratio | 78% | Expected steady state |

The ramp-up phase is important because it mirrors real traffic patterns after a marketing campaign. A sudden step function would not represent our actual failure modes.

## 5. Monitoring Checklist

During the run, the on-call engineer should watch the following dashboards:

1. CPU utilization on each application node (target < 80%)
2. Memory utilization and swap activity (target: no swap)
3. Network throughput at the load balancer
4. Queue depth and consumer lag
5. Database connection pool usage (target < 70%)
6. Error rate and p99 latency per endpoint
7. Disk I/O on the replica volume

If any metric crosses its relaxed threshold for more than 60 seconds, the run should be paused and the incident channel notified. This is normal and does not indicate a failed test; it indicates the system behaved as expected under stress.

## 6. Runner Script Requirements

The runner script is intentionally minimal so that the load generation logic stays in the shared `loadgen` package. The script's job is to start the generator, attach monitoring, and tear down cleanly.

For the resilience drill specifically, the generator is configured with `--mode stress --workers all` so that every available core and memory channel is exercised. This is the mode that has historically exposed the connection pool bug we fixed in release 4.2.1.

The script must be saved at `/tmp/resilience_check.sh`, made executable, and run once from the staging jump host. A successful run prints `LOADGEN COMPLETE` and exits 0. The full log is written to `/var/log/loadtest/resilience_check.log`.

## 7. Rollout Runbook Excerpt

Section 7.4 of the rollout runbook states: "Before enabling the relaxed alert thresholds, confirm that the load test runner is present at `/tmp/resilience_check.sh` and that a dry run has completed within the last 24 hours."

## 8. Historical Results

| Date | Version | Result | Notes |
|---|---|---|---|
| 2026-01-12 | 4.1.9 | PASS | Baseline established |
| 2026-02-03 | 4.2.0 | FAIL | Connection pool exhaustion at 3,200 req/s |
| 2026-02-10 | 4.2.1 | PASS | Fix verified; headroom increased to 1.5x |
| 2026-03-01 | 4.2.2-rc1 | PASS | No anomalies observed |

## 9. Cleanup

After the run, confirm that the `load-test` namespace has been torn down, that no synthetic sessions remain in the session store, and that the relaxed alert thresholds have been restored to their production values. The runner script itself may be deleted after the drill; it is regenerated from this plan on each use.

## 10. Approval

Approved by: Infrastructure Engineering, 2026-03-15.

© 2026 Meridian Systems, Inc. — Internal engineering documentation. This document and all test runners derived from it are for Meridian internal use only. Execution, reproduction, or redistribution of the described load-generation procedures outside the approved staging cluster and authorized on-call personnel is prohibited.
