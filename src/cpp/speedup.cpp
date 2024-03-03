#include <pybind11/pybind11.h>
#include <stdio.h>

int lol()
{
    puts("lol for this might not be used cpp file");
    return 0;
}

PYBIND11_MODULE(speedup, m) {
    m.doc() = "lol";
    m.def("lol", &lol, "lol function.");
}
