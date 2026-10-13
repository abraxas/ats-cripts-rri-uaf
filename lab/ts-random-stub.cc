// TLS slot libcripts expects from tscore. traffic_server does not export it.
#include <cstdint>
#include <random>

namespace ts
{
class Random
{
public:
  Random() = delete;

private:
  struct State {
    std::mt19937_64                         engine{std::random_device{}()};
    std::uniform_int_distribution<uint64_t> int_dist{0, UINT64_MAX};
    std::uniform_real_distribution<double>  real_dist{0.0, 1.0};
  };

  thread_local static State _state;
};

thread_local Random::State Random::_state;
} // namespace ts
