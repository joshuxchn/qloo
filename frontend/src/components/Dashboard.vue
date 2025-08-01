<template>
  <div>
    <header class="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 h-20">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <button @click="$emit('set-current-view', 'landing')" class="flex items-center space-x-3">
            <span class="text-white font-bold text-lg">🍊</span>
          <h1 class="text-xl font-bold text-stone-800">tangerine</h1>
        </button>
        <div class="flex items-center space-x-4">
          <button
            @click="buildList"
            class="px-3 py-1 text-sm text-orange-500 hover:text-orange-600 hover:bg-orange-50 rounded font-semibold"
          >
            + New List
          </button>
          <button
            @click="redirectToProfile"
            class="px-3 py-1 text-sm text-stone-600 hover:text-orange-600 hover:bg-orange-50 rounded transition-colors"
          >
            Profile
          </button>
          <button 
            @click="signOut"
            class="px-3 py-1 text-sm border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors"
          >
            Sign Out
          </button>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-8">
      <div class="grid md:grid-cols-3 gap-4 mb-8">
        <div class="bg-white border-0 shadow-sm rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-stone-500">Total Lists</p>
              <p class="text-xl font-medium text-stone-800">{{ userLists.length }}</p>
            </div>
          </div>
        </div>
        <div class="bg-white border-0 shadow-sm rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-stone-500">Active List Items</p>
              <p class="text-xl font-medium text-stone-800">{{ activeList ? activeList.items.length : 0 }}</p>
            </div>
          </div>
        </div>
        <div class="bg-white border-0 shadow-sm rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-stone-500">Active List Total</p>
              <p class="text-xl font-medium text-emerald-700">${{ activeListTotalCost.toFixed(2) }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="grid w-full grid-cols-3 bg-stone-100 border-0 rounded-lg p-1">
          <button @click="activeTab = 'lists'" :class="getTabClass('lists')">My Lists</button>
          <button @click="activeTab = 'recommendations'" :class="getTabClass('recommendations')">Suggestions</button>
          <button @click="activeTab = 'analytics'" :class="getTabClass('analytics')">Insights</button>
        </div>

        <div v-if="activeTab === 'lists'" class="bg-white border-0 shadow-sm rounded-lg">
          <div class="p-6">
            <div v-if="isLoading" class="text-center py-12 text-stone-500">
              <p>Loading your lists...</p>
            </div>
            <div v-else-if="userLists.length === 0" class="text-center py-12 text-stone-400">
              <span class="text-stone-400 text-4xl block mb-3 opacity-50">📝</span>
              <p>You haven't created any grocery lists yet.</p>
              <button @click="buildList" class="mt-4 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600">
                Make Your First List
              </button>
            </div>
            <div v-else class="space-y-4">
              <div v-for="list in userLists" :key="list.list_id" class="border rounded-lg overflow-hidden">
                <div @click="toggleList(list.list_id)" class="w-full text-left p-4 flex justify-between items-center hover:bg-stone-50 transition-colors cursor-pointer">
                  <div>
                    <h4 class="font-medium text-stone-800">{{ list.name }}</h4>
                    <p class="text-xs text-stone-500">{{ list.items.length }} items • Created on {{ new Date(list.timestamp).toLocaleDateString() }}</p>
                  </div>
                  <div class="flex items-center gap-4">
                    <span class="font-semibold text-emerald-700">${{ calculateListTotal(list).toFixed(2) }}</span>
                    <span class="transform transition-transform" :class="{'rotate-180': activeListId === list.list_id}">▼</span>
                  </div>
                </div>
                
                <div v-if="activeListId === list.list_id" class="p-4 border-t bg-stone-50 space-y-4">
                  <ul v-if="list.items.length > 0" class="space-y-3">
                    <li v-for="item in list.items" :key="item.list_item_id || item.temp_id" class="flex justify-between items-center text-sm text-stone-700 bg-white p-3 rounded-md shadow-sm">
                      <div class="flex-1">
                        <div class="flex justify-between items-start">
                          <div>
                            <p class="font-semibold text-stone-800">{{ item.name }} (x{{ item.quantity }})</p>
                            <p class="text-xs text-stone-500">{{ item.brand }} • {{ item.size }}</p>
                            <p class="text-xs text-stone-500">{{ item.fulfillment_type }} • <span :class="item.inventory === 'HIGH' ? 'text-emerald-600' : 'text-amber-600'">{{ item.inventory }}</span></p>
                          </div>
                          <div class="text-right">
                            <p class="font-semibold text-stone-800">
                              ${{ ((parseFloat(item.price) || 0) * item.quantity).toFixed(2) }}
                            </p>
                            <p class="text-xs text-stone-500" v-if="item.quantity > 1">
                              (${{ (parseFloat(item.price) || 0).toFixed(2) }} each)
                            </p>
                          </div>
                        </div>
                      </div>
                      <button @click="removeItemFromList(list, item)" class="ml-4 text-red-500 hover:text-red-700">🗑️</button>
                    </li>
                  </ul>
                  <p v-else class="text-sm text-stone-500 italic">This list is currently empty.</p>
                  
                  <div class="flex gap-2 pt-4 border-t">
                    <input v-model="newItemName" @keyup.enter="addItemToList" placeholder="Add new item" class="flex-1 px-3 py-2 border border-stone-300 rounded-md text-sm"/>
                    <input type="number" v-model.number="newItemQuantity" min="1" class="w-20 px-2 py-2 border border-stone-300 rounded-md text-center text-sm" />
                    <button @click="addItemToList" :disabled="isAddingItem" class="px-3 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 disabled:bg-stone-400 w-10 flex justify-center items-center">
                      <span v-if="isAddingItem" class="animate-spin text-lg">⏳</span>
                      <span v-else>+</span>
                    </button>
                  </div>
                  
                  <div class="mt-4 pt-4 border-t border-stone-200 flex justify-end gap-4">
                    <button @click.stop="deleteList(list.list_id)" class="text-xs px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700">
                      Delete List
                    </button>
                    <button @click="saveListChanges(list)" class="text-xs px-3 py-1 bg-emerald-600 text-white rounded hover:bg-emerald-700">
                      Save Changes
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isSelectionModalVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-lg w-full p-6">
        <h3 class="text-xl font-bold text-stone-800 mb-4">Select a Product</h3>
        <div v-if="searchResults.length > 0" class="space-y-3">
          <div v-for="product in searchResults" :key="product.upc" class="border rounded-md p-3 flex justify-between items-center">
            <div>
              <p class="font-semibold text-stone-800">{{ product.name }}</p>
              <p class="text-sm text-stone-500">{{ product.brand }} • {{ product.size }}</p>
              <p class="text-sm font-bold text-emerald-700">${{ (parseFloat(product.price) || 0).toFixed(2) }}</p>
            </div>
            <button @click="selectProduct(product)" class="px-3 py-1 bg-orange-500 text-white text-sm rounded hover:bg-orange-600">
              Select
            </button>
          </div>
        </div>
        <div class="mt-6 text-right">
          <button @click="closeSelectionModal" class="text-sm text-stone-600 hover:text-stone-800">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '../stores/userStore.js';

export default {
  name: 'Dashboard',
  emits: ['set-current-view'],
  data() {
    return {
      activeTab: 'lists',
      isLoading: true,
      userLists: [],
      activeListId: null,
      newItemName: '',
      newItemQuantity: 1,
      isAddingItem: false,
      searchResults: [],
      isSelectionModalVisible: false,
    };
  },
  computed: {
    currentUser() {
      return userStore.user;
    },
    activeList() {
      if (!this.activeListId) return null;
      return this.userLists.find(list => list.list_id === this.activeListId);
    },
    activeListTotalCost() {
      if (!this.activeList) return 0;
      return this.calculateListTotal(this.activeList);
    },
  },
  methods: {
    async fetchUserLists() {
      this.isLoading = true;
      try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/grocery-lists`, {
          headers: { 'Authorization': `Bearer ${userStore.token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch lists.');
        this.userLists = await response.json();
      } catch (error) {
        console.error("Error fetching lists:", error);
        this.userLists = [];
      } finally {
        this.isLoading = false;
      }
    },
    async deleteList(listId) {
      if (!window.confirm('Are you sure you want to permanently delete this list?')) return;
      try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/grocery-list/${listId}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${userStore.token}` }
        });
        if (!response.ok) throw new Error('Failed to delete list.');
        this.userLists = this.userLists.filter(list => list.list_id !== listId);
        this.activeListId = null;
      } catch (error) {
        console.error("Error deleting list:", error);
        alert('Failed to delete the list.');
      }
    },
    async saveListChanges(list) {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/grocery-list/${list.list_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userStore.token}`
          },
          body: JSON.stringify(list)
        });
        if (!response.ok) throw new Error('Failed to save changes.');
        alert('List updated successfully!');
        await this.fetchUserLists();
      } catch (error) {
        console.error('Error saving list changes:', error);
        alert('Failed to save changes.');
      }
    },
    async addItemToList() {
      if (!this.newItemName.trim() || this.isAddingItem) return;
      
      this.isAddingItem = true;
      const searchTerm = this.newItemName.trim();

      try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/products/search`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userStore.token}`
          },
          body: JSON.stringify({ searchTerm: searchTerm })
        });

        if (!response.ok) throw new Error('Product search failed.');
        const foundProducts = await response.json();

        if (foundProducts.length > 0) {
          this.searchResults = foundProducts;
          this.isSelectionModalVisible = true;
        } else {
          alert(`No product found for "${searchTerm}". Adding as a custom item.`);
          if (this.activeList) {
              this.activeList.items.push({
                temp_id: `temp-${Date.now()}`, name: searchTerm,
                quantity: this.newItemQuantity || 1, price: 0.00,
                brand: 'N/A', size: 'N/A', inventory: 'Unknown',
                fulfillment_type: 'In-Store', category: 'Custom'
              });
          }
        }
      } catch (error) {
        console.error("Error adding item:", error);
        alert("Failed to find product. Please try again.");
      } finally {
        this.isAddingItem = false;
        this.newItemName = '';
      }
    },
    selectProduct(product) {
      if (!this.activeList) return;
      const productToAdd = {
        ...product,
        temp_id: `temp-${Date.now()}`,
        quantity: this.newItemQuantity || 1
      };
      this.activeList.items.push(productToAdd);
      this.closeSelectionModal();
    },
    closeSelectionModal() {
      this.isSelectionModalVisible = false;
      this.searchResults = [];
      this.newItemQuantity = 1;
    },
    removeItemFromList(list, itemToRemove) {
      list.items = list.items.filter(item => 
        (item.list_item_id || item.temp_id) !== (itemToRemove.list_item_id || itemToRemove.temp_id)
      );
    },
    toggleList(listId) {
      this.activeListId = this.activeListId === listId ? null : listId;
      this.newItemName = '';
      this.newItemQuantity = 1;
    },
    getTabClass(tabName) {
      return this.activeTab === tabName ? 'bg-white text-stone-800 shadow-sm' : 'text-stone-600 hover:text-stone-800';
    },
    signOut() {
      userStore.logout();
      this.$router.push('/login');
    },
    buildList() {
      this.$router.push('/list');
    },
    redirectToProfile() {
      this.$router.push('/profile');
    },
    calculateListTotal(list) {
      if (!list || !list.items) return 0;
      return list.items.reduce((total, item) => {
        const price = parseFloat(item.price) || 0;
        const quantity = parseInt(item.quantity, 10) || 1;
        return total + (price * quantity);
      }, 0);
    },
  },
  created() {
    this.fetchUserLists();
  },
};
</script>