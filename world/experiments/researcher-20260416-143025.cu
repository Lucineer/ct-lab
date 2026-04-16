// Auto-generated experiment: researcher-20260416-143025
// Claim: DCS benefit is inversely proportional to perception range
// agents=512, food=500, threshold=1.5x
#include <cstdio>
#include <cstdint>
struct Agent { float x, y, energy, fitness; int food_collected; };
__global__ void experiment_kernel(Agent* agents, int seed) {
    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    if (tid >= 512) return;
    // TODO: hypothesis-specific behavior
    agents[tid].fitness = agents[tid].food_collected;
}
int main() {
    Agent* d_a; Agent* h_a = new Agent[512];
    cudaMalloc(&d_a, 512 * sizeof(Agent));
    cudaMemcpy(d_a, h_a, 512 * sizeof(Agent), cudaMemcpyHostToDevice);
    experiment_kernel<<<(512+255)/256, 256>>>(d_a, 42);
    cudaDeviceSynchronize();
    cudaMemcpy(h_a, d_a, 512 * sizeof(Agent), cudaMemcpyDeviceToHost);
    float total = 0;
    for (int i = 0; i < 512; i++) total += h_a[i].fitness;
    printf("Avg fitness: %f, Threshold: 1.5x\n", total/512);
    cudaFree(d_a); delete[] h_a; return 0;
}
