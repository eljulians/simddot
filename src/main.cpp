#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <vector>

double dot(const std::vector<double> &a, const std::vector<double> &b) {
    double result = 0.0;
    for (size_t i = 0; i < a.size(); ++i) {
        result += a[i] * b[i];
    }
    return result;
}

PYBIND11_MODULE(_core, m) {
    m.def("dot", &dot, "Dot product of two vectors");
}
