Phones = ["Phone, BPCM Compact 29.99", "Phone, BPSH Clam Shell 49.99", "Phone, RPSS RoboPhone - 5-inch screen and 64GB memory 199.99", "Phone, RPLL RoboPhone - 6-inch screen and 256GB memory 499.99", "Phone, YPLS Y-Phone Standard - 6-inch screen and 64GB memory 549.99", "Phone, YPLL Y-Phone Deluxe - 6-inch screen and 256GB memory 649.99"]
phones_new = [y[0].strip(",") for x in Phones for y in x.split(" ")]
print(phones_new)
