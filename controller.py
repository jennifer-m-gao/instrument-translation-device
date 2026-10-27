import asyncio
from tapsdk import (
    DeviceFeatures,
    InputModeController,
    ModelTypes,
    VisionSensorOpModes,
    connect,
)


def on_tap(identifier, tapcode):
    # tapcode is int 1..31 — bit0=thumb … bit4=pinky
    code = tapcode[0] if isinstance(tapcode, (list, tuple)) else tapcode
    print(f"{identifier} tapped {code} (0b{int(code):05b})")


async def main():
    sdk = await connect()
    sdk.register_tap_events(on_tap)
    await sdk.start()
    if hasattr(sdk, "set_input_mode"):
        await sdk.set_input_mode(InputModeController())
    else:
        await sdk.set_feature(DeviceFeatures.MODEL_DETECTION, True)
        await sdk.set_vision_sensor_model(ModelTypes.TAPPING)
        await sdk.set_vision_sensor_op_mode(VisionSensorOpModes.TRIGGER)

    print("Waiting for taps… (Ctrl+C to quit)")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())