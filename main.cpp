#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "RadioControlProtocolCpp/rcLib.hpp"

namespace py = pybind11;

#define NAMEOF(x) #x
#define FUNC(x) NAMEOF(x), &rcLib::Package::x


auto encodeWrapper(rcLib::Package &pkg) -> std::vector<uint8_t> {
    return {pkg.getEncodedData(), pkg.getEncodedData() + pkg.encode()};
}

PYBIND11_MODULE(rc_lib, m) {
    py::class_<rcLib::Package>(m, NAMEOF(Package))
        .def(py::init<>())
        .def(py::init<uint16_t, uint8_t>())
        .def(FUNC(decode))
        .def(NAMEOF(encode), encodeWrapper)
        .def(FUNC(setChannel))
        .def(FUNC(getChannel))
        .def(FUNC(getChannelCount))
        .def(FUNC(getResolution))
        .def(FUNC(getDeviceId))
        .def(FUNC(setDeviceId))
        .def(FUNC(isChecksumCorrect))
        .def(FUNC(isMesh))
        .def(FUNC(setMeshProperties))
        .def(FUNC(needsForwarding))
        .def(FUNC(countNode))
        .def(FUNC(isDiscoverMessage))
        .def(FUNC(isDiscoverResponse))
        .def(FUNC(setDiscoverMessage))
        .def(FUNC(makeDiscoverResponse));
    m.def(FUNC(setTransmitterId));
    m.def(FUNC(getTransmitterId));
}
