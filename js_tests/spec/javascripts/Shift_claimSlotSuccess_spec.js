describe("Shift.claimSlotSuccess", function() {
  beforeAll(function() {
      window.django_user = new Backbone.Model({id: 1, display_name: "test user", shifts: []});
  });

  afterAll(function() {
      delete window.django_user;
  });
  it("should be create a new Slot model and add it to the collection.", function() {
    var shift = new app.Shift({id: 3, claimed_slots: []});
    expect(shift.get("claimed_slots").length).toEqual(0);
    shift.claimSlotSuccess({'id': 10});
    expect(shift.get("claimed_slots").length).toEqual(1);
  });
});
