describe("Shift.cliamSlotSuccess", function() {
  it("should be create a new Slot model and add it to the collection.", function() {
    var shift = new app.Shift({id: 3, claimed_slots: []});
    expect(shift.get("claimed_slots").length).toEqual(0);
    shift.cliamSlotSuccess({'id': 10});
    expect(shift.get("claimed_slots").length).toEqual(1);
  });
});
