package Common;

enum EnumTest
{
    ENUM_TEST_INVALID    = 0;
    ENUM_TEST_A            = 1;
    ENUM_TEST_B            = 2;
}

message StructTest
{
    optional EnumTest type    = 1 [default = ENUM_TEST_INVALID];
    optional float    val    = 2;
}
